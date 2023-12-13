# Copyright 2023, QC Design GmbH and the plaquette contributors
# SPDX-License-Identifier: Apache-2.0
r"""Decoders and related functions.

All decoders in ``plaquette`` have the same interface, and adding new
ones should be straightforward. Here we detail the inner workings of
the base class that all decoder inherit from: :class:`AbstractDecoder`.

This class takes care of some common tasks that all decoder
subclasses can take advantage of.


Decoding graph initialization
-----------------------------

First, it creates the **decoding** graph from the code given as an
input. This decoding graph is stored in :attr:`.AbstractDecoder._decoding_graph`,
and it's marked private because in principle no user should ever need
to interact with it, **but** decoder subclasses will find it useful
to translate its structure to whatever is necessary for them to work.
The decoding graph makes no distinction between "X" and "Z" components.

.. seealso::

   :class:`.DecodingGraph`.

.. important::

   If decoders cannot deal with multiple components at once or with
   isolated vertices they then they MUST deal with this fact on its own.

Since decoders can deal with multiple round of measurements of the
same code, each decoder needs to know the number of rounds, which is
given during initialization (see :meth:`AbstractDecoder.__init__`). At each round
:math:`r`, starting at 0, nodes are indexed always in the same way,
but with an offset :math:`\delta = rN`, where :math:`N` is the
number of both real and *virtual* ancilla qubits.

The decoding graph will also add **a new virtual node** (i.e. a node
that does not represent a physical qubit, neither data nor ancilla)
when any error mechanism would corrupt only one syndrome value
instead of a pair. These virtual nodes are collected into the
attribute :attr:`_virtual_ancillas`. A similar attribute exists for
:attr:`_virtual_edges`.

Syndrome and erasure information
--------------------------------

Syndrome (erasure) information is an array of booleans which
indicate whether the corresponding ancilla (data) qubit
was affected by an error (erasure). Each syndrome bit corresponds to the
stabilizer measurement defined in the :class:`.Code` used to initialize
the decoder, such that ``syndrome[i]`` corresponds to the measurement
information of ``Code.stabilizers[i]``.
"""
import abc
import copy
import json
import pathlib
import typing as t
import warnings

import fusion_blossom as fb
import numpy as np
import pymatching

from plaquette import codes, errors, graph, pauli

NodeIndex = t.NewType("NodeIndex", int)
"""Typing helper to mark specific ints as node indices."""
EdgeIndex = t.NewType("EdgeIndex", int)
"""Typing helper to mark specific ints as edge indices."""


def check_success(
    code: codes.Code,
    correction: pauli.Tableau,
    logical_op_toggle: np.ndarray,
    logical_ops: str,
):
    """Compare measured with predicted logical operator results.

    This function compares measured logical operators with the prediction from the
    decoder. If they match, this test of QEC can be considered successful.

    Args:
        code: Code definition containing logical operators
        correction: Correction Pauli operator from the decoder
        logical_op_toggle: XOR between logical op. measurement result
            before and after QEC
        logical_ops: Specify which logical operators were measured. If
            you pass a string ``"XZX"`` it means that you measured, and
            want to check, the X operator on the first logical qubit,
            the Z operator on the second and so on. There is no
            shorthand at the moment to check a *specific* logical qubit,
            you always have to start from the first.

    Returns:
        an array of booleans, indicating whether each logical operator
        was preserved/corrected.

    Notes:
        This function does the following:

        * Flip logical operators according to the correction Pauli
          frame from the decoder.
        * Check whether the predicted signs of logical operators agree
          with measurement results.

        For more details, see :doc:`/quickstart`.
    """
    decoder_prediction = np.zeros_like(logical_op_toggle, dtype="u1")

    for i, op in enumerate(logical_ops):
        assert (
            op in "XZ"
        ), "currently only X and Z logical operators are supported on a logical qubit"
        op_idx = i + code.num_logical_qubits if op == "Z" else i
        log_op = code.logical_ops[op_idx]

        # FIXME: op_toggle comes from MeasurementSample, which needs updating to
        #  calculate stuff only for a single logical operator at a time
        assert pauli.count_qubits(correction)[0] == code.num_data_qubits
        decoder_prediction[i] = (pauli.commutator_sign(log_op, correction)).ravel()

    return np.array(
        [a == b for a, b in zip(logical_op_toggle, decoder_prediction)], dtype=bool
    )


def calculate_LER_qubitwise(success: np.ndarray) -> list[float]:
    """Calculate qubit wise logical error rate.

    Args:
        success: An 2d numpy array of shape (reps, # logical qubits)

    Returns:
         A 1-d array of shape (# logical qubits, )
    """
    return 1 - np.count_nonzero(success, axis=0) / np.shape(success)[0]


class AbstractDecoder(abc.ABC):
    """The base class/interface for all decoders."""

    def __init__(
        self, code: codes.Code, error_data: errors.ErrorDataDict, n_rounds: int
    ):
        """Create a decoder tailored on a specific code and for the given rounds.

        Args:
            code: the code whose results you want to decode.
            error_data: information about the error model used. Used to
                calculate edge weights of the decoding graph.
            n_rounds: number of measurement rounds your code went through.

        Notes:
            **Do not** construct a new decoder each time you want to decode a
            new syndrome. If the underlying code and number of measurements do
            not change, neither does the decoding graph.

            Using error probabilities above 50% will results in negative weights, which
            will most likely cause problems decoders are not equipped to deal with.
        """
        self.selection: t.Sequence[EdgeIndex] = tuple()
        """The cached selection from the decoder.

        After calling :meth:`decode`, this attribute will be set to the
        results of the decoder. Useful mainly for debugging or
        visualisation purposes.
        """
        self._code = code
        self._n_rounds = n_rounds
        self._data_qubit_index_for_edge: dict[EdgeIndex, NodeIndex] = {}
        """A mapping of edges to qubit indices.

        This dict has as many elements as the decoding graph has edges.
        The i-th edge connects two stabilizer checks whose outcomes have been
        flipped by the action of an error on the data qubit whose index is the
        i-th element of this list.
        """
        # Take a list of all possible error operators that could act on a
        # specific data qubit
        error_operators = [
            pauli.single_qubit_pauli_operator(o, i, self._code.num_data_qubits)
            for o in "XZ"
            for i in range(self._code.num_data_qubits)
        ]
        self._virtual_ancillas: list[NodeIndex] = []
        """Ancilla indices which do not belong to the original code graph."""
        self._virtual_edges: list[EdgeIndex] = []
        """Decoding graph edges *indices* containing virtual ancillas."""
        edges: list[graph.Edge] = list()
        """Edges of the decoding graph, both virtual and not."""
        self._edges_weights: np.ndarray[t.Any, np.uint32]  # assigned below
        """A list of weights for each edge in the decoding graph."""
        commutator_signs = pauli.commutator_sign(
            error_operators, self._code.stabilizers
        )
        """2D array telling whether the i-th error commutes with the j-th stabilizer.

        For each error operator, we compute the commutator sign with all
        possible stabilizers. An **edge** in the decoding graph can only exist
        between stabilizer measurements that **do not** commute with the given
        error operator.

        This holds the commutator sign of the given operator pointed
        by op_idx with all stabilizers. For a given index ``i``,
        ``commutator_signs[i]`` is 0 if ``code.stabilizers[i]``
        commutes with ``error_operators[op_idx]``.
        """

        # If there are dangling edges, we need to add fake/virtual ancillas
        # but in order to layer the various rounds properly, we need to know
        # in advance how many virtual ancillas we need
        num_virtual_ancilla_vertices: int = np.count_nonzero(
            np.array(list(map(lambda x: len(np.nonzero(x)[0]), commutator_signs))) == 1
        )
        self._nodes_per_round = (
            num_virtual_ancilla_vertices + self._code.num_stabilizers
        )
        r"""Number of nodes per round necessary to build the decoding graph.

        The decoding graph for a code is made by layering the code graph on top
        of it self as many times as there are measurement rounds. The decoding
        graph will clearly have many more nodes than the graph describing the
        code itself, but each node will have the same index per round, assuming
        we take the modulo with the total number of nodes per round.

        As an example, the distance-3 rotated planar code has :math:`A` real
        ancilla nodes, plus :math:`V`
        virtual ancillas (to avoid dangling edges), so there's :math:`N = A+V`
        nodes per round.

        At each round, we offset the next node index in the decoding graph by
        :math:`N r`, where :math:`r` is the current round number. In this way,
        whenever we want to know which ancilla measurement we are referring to
        with a given index :math:`j` in the decoding graph, we can obtain
        this information by :math:`a = j \bmod N`.
        """
        nodes_data: list[graph.Node | None] = [None] * (
            self._nodes_per_round * n_rounds
        )
        """Decoding graph metadata, mostly used for visualization."""

        self._last_decoded_syndrome: t.Sequence[bool] = []
        """Last syndrome passed to the :meth:`.decode` method.

        This is the syndrome passed to :meth:`.select_edges`, so after any
        transformation done in the :meth:`.decode` method.
        """
        self._last_decoded_erasure: t.Sequence[bool] = []
        """Last erasure information passed to the :meth:`.decode` method.

        This is the erasure passed to :meth:`.select_edges`, so after any
        transformation done in the :meth:`.decode` method.
        """

        # region Edge weights calculation

        # First we use the information in error_data to construct the
        # edges' weights. Multiple error mechanisms acting on the same
        # qubit will be merged into an effective "fault" probability
        # that will be used to calculate the effective weights.
        #
        # Faults are always reduced to effectively three mechanisms,
        # because this is what decoders understand: X errors, Z errors
        # or measurement errors. Y errors are not included because they
        # are "split" among X and Z errors appropriately. Erasure errors
        # are effectively half the time X errors and half the time Z
        # errors.

        eff_error_probabilities: dict[str, dict[NodeIndex, float]] = {
            "x": {},
            "z": {},
            "measurement": {},
        }
        pauli_errors = error_data.get("pauli", None)
        measurement_errors = error_data.get("measurement", None)
        for v in code.data_qubit_indices:
            v = t.cast(NodeIndex, v)
            # data qubits are affected by either pauli or erasure errors
            p_x = 0.0
            p_z = 0.0
            if pauli_errors and (qubit_errors := pauli_errors.get(v)):
                # probabilities given by the user
                _px = qubit_errors.get("x", 0.0)
                _py = qubit_errors.get("y", 0.0)
                _pz = qubit_errors.get("z", 0.0)
                # Effective probabilities that the decoders will use for weights.
                # We also assume that all error mechanisms are independent (i.e. it
                # could be that BOTH an X and a Z are applied on the same qubit)
                p_x += _px * (1 - _py) + _py * (1 - _px)
                p_z += _pz * (1 - _py) + _py * (1 - _pz)
            eff_error_probabilities["x"][v] = p_x
            eff_error_probabilities["z"][v] = p_z

        for v in range(code.num_stabilizers):
            # and now we add error probabilities to ancilla qubits for
            # the time-like edges' weights
            v = t.cast(NodeIndex, v + code.num_data_qubits)
            p_m = 0.0
            if measurement_errors and (meas_error := measurement_errors.get(v)):
                p_m = meas_error.get("p", 0.0)
            eff_error_probabilities["measurement"][v] = p_m
        # endregion

        edges_weights: list[float] = list()
        # Used later to calculate positions of virtual ancillas, but
        # we cache it here for performance reasons
        data_qubits_coords = [
            code.tanner_graph.nodes[n].pos for n in code.data_qubit_indices
        ]
        data_qubits_coords_incomplete = not all(data_qubits_coords)
        if not any([i is None for i in data_qubits_coords]):
            data_qubits_center_of_mass = graph.center_of_mass(data_qubits_coords)
        else:
            data_qubits_center_of_mass = graph.Position(x=1, y=0, z=0)

        # The decoding graph takes into account also all measurement rounds, and
        # we only need to create edges between the same data qubits across rounds.
        # This means that you can always recover the data qubit index in the code
        # from the decoding graph by taking its index % code.num_data_qubits.
        for meas_round in range(self._n_rounds):
            # region Single-layer construction
            # We also need to "fix" dangling edges, where an error operator
            # anti-commutes with only one stabilizer instead of two. We use
            # virtual/fake ancillas, whose indices lie out of the range
            # of indices used by the code
            next_virtual_ancilla_idx = self._code.num_stabilizers
            for op_idx, comm_signs in enumerate(commutator_signs):
                non_commuting_stabilizers = np.nonzero(comm_signs)[0]

                if not (n := len(non_commuting_stabilizers)):
                    # We skip error operators that commute with everything, they will
                    # not contribute to the decoding graph
                    continue
                elif n == 1:
                    # This is a "dangling edge", and we connect it with a virtual
                    # node whose index is defined as the total number of qubits of
                    # the code (data + ancilla) such that it can never be mistaken
                    # for a "real" qubit index
                    non_commuting_stabilizers = (
                        non_commuting_stabilizers[0],
                        next_virtual_ancilla_idx,
                    )
                    next_virtual_ancilla_idx += 1
                elif n > 2:
                    # Currently we don't support hyper-edges, so we need to
                    # avoid this case
                    raise ValueError(
                        f"a qubit being shared among {n} stabilizers "
                        "(a hyper-edge in the decoding graph) is not supported"
                    )

                # Check which factor we need to assign to this edge
                factors = [
                    (k, v)
                    for k, v in pauli.pauli_to_dict(error_operators[op_idx]).items()
                ]
                assert len(factors) == 1, "error operator must act only on one qubit"

                # link decoding graph edge with the corresponding data qubit in
                # the code's graph
                data_qubit_index = t.cast(NodeIndex, factors[0][0])
                pauli_factor = factors[0][1]

                # by offsetting the stabilizer index by num_nodes*meas_round we
                # make sure that we can convert from decoding graph index to real qubit
                # (ancilla) index in a simple way:
                #
                #   ancilla_index = dec_graph_index%num_nodes
                vert_a: NodeIndex = (
                    self._nodes_per_round * meas_round + non_commuting_stabilizers[0]
                )
                vert_b: NodeIndex = (
                    self._nodes_per_round * meas_round + non_commuting_stabilizers[1]
                )
                edges.append(graph.Edge(a=vert_a, b=vert_b, type=pauli_factor.name))

                edge_idx = t.cast(EdgeIndex, len(edges) - 1)
                self._data_qubit_index_for_edge[edge_idx] = data_qubit_index
                # recover error probability for the error specified by the edge
                # factor and by which data qubit this edge "crosses", or alternatively
                # by which faulty data qubit would "create" this edge
                p = eff_error_probabilities[pauli_factor.name.lower()][
                    self._data_qubit_index_for_edge[edge_idx]
                ]

                if p == 0.0:
                    edges_weights.append(float("inf"))
                elif p == 1.0:
                    edges_weights.append(-float("inf"))
                elif 0 < p < 1:
                    edges_weights.append(-np.log(p / (1 - p)))
                else:
                    raise ValueError(
                        f"The p={p} calculating edge weights is not between 0 and 1"
                    )
                # Some decoders like to know which one is a real ancilla and which one
                # is not, so we keep track of them.
                #
                # Since virtual ancillas are added at each round, we need to check
                # that the current vertex index being added exceeds the correct amount
                # of nodes indices to be marked as virtual *in that round*
                if (vert_a % self._nodes_per_round) >= code.num_stabilizers:
                    self._virtual_ancillas.append(vert_a)
                    self._virtual_edges.append(t.cast(EdgeIndex, len(edges) - 1))
                    nodes_data[vert_b] = copy.deepcopy(
                        code.tanner_graph.nodes[
                            (vert_b % self._nodes_per_round) + code.num_data_qubits
                        ]
                    )
                elif (vert_b % self._nodes_per_round) >= code.num_stabilizers:
                    self._virtual_ancillas.append(vert_b)
                    self._virtual_edges.append(t.cast(EdgeIndex, len(edges) - 1))
                    nodes_data[vert_a] = copy.deepcopy(
                        code.tanner_graph.nodes[
                            (vert_a % self._nodes_per_round) + code.num_data_qubits
                        ]
                    )
                else:
                    nodes_data[vert_a] = copy.deepcopy(
                        code.tanner_graph.nodes[
                            (vert_a % self._nodes_per_round) + code.num_data_qubits
                        ]
                    )
                    nodes_data[vert_b] = copy.deepcopy(
                        code.tanner_graph.nodes[
                            (vert_b % self._nodes_per_round) + code.num_data_qubits
                        ]
                    )

                # FIXME: this assumes that the code is always a 2D surface that can be
                #  offset in the Z direction. This is wrong, and we should offset
                #  each round of measurements by the "biggest Z displacement" of the
                #  code itself.
                if (nd := nodes_data[vert_a]) is not None and nd.pos is not None:
                    nd.pos.z = meas_round
                if (nd := nodes_data[vert_b]) is not None and nd.pos is not None:
                    nd.pos.z = meas_round

            # endregion
            # region Time-like layer linking
            # Now we also link the current layer of ancillas to the previous round
            if meas_round > 0:
                for ancilla in range(code.num_stabilizers):
                    edges.append(
                        graph.Edge(
                            a=self._nodes_per_round * meas_round + ancilla,
                            b=self._nodes_per_round * (meas_round - 1) + ancilla,
                            type=pauli.Factor.I.name,
                        )
                    )
                    # by default this time-like edge has no error probability, because
                    # we assume that it's a virtual ancilla
                    p = 0.0
                    if ancilla < code.num_stabilizers:
                        # if it is a real ancilla instead, it might have a measurement
                        # error probability greater than zero
                        ancilla = t.cast(NodeIndex, ancilla + code.num_data_qubits)
                        p = eff_error_probabilities["measurement"][ancilla]

                    if p == 0.0:
                        edges_weights.append(float("inf"))
                    elif p == 1.0:
                        edges_weights.append(-float("inf"))
                    elif 0 < p < 1:
                        edges_weights.append(-np.log(p / (1 - p)))
                    else:
                        raise ValueError(
                            f"The p={p} calculating edge weights is not between 0 and 1"
                        )
            # endregion

        # region Virtual ancilla placements
        # Now the last thing to do is to *place* the virtual ancillas
        # for visualization. This can only happen if all data qubits
        # have an assigned position themselves.
        if not data_qubits_coords_incomplete:
            for v_edge in self._virtual_edges:
                a, b = edges[v_edge].a, edges[v_edge].b
                # sort which one is the virtual ancilla and which is not
                if a % self._nodes_per_round > code.num_stabilizers:
                    v_anc = a
                    r_anc = b
                else:
                    v_anc = b
                    r_anc = a
                # We find now a radial vector starting from the code
                # center of mass to the real ancilla position. We will
                # place the virtual ancilla along the direction of this
                # vector, with a small offset
                # TODO: make the offset configurable
                nd = code.tanner_graph.nodes[
                    r_anc % self._nodes_per_round + code.num_data_qubits
                ]
                assert nd is not None, "node data missing"

                # x, y, z = coords
                r_pos = nd.pos
                v_pos = (
                    t.cast(graph.Position, r_pos) - data_qubits_center_of_mass
                ).unit() + r_pos
                v_pos.z = r_anc // self._nodes_per_round

                nodes_data[v_anc] = graph.Node(
                    pos=v_pos, type=codes.QubitType.virtual.name
                )
        # endregion

        # note: below is hack to ensure that decoding graph still works without the
        # coordinate information.
        for i in range(len(nodes_data)):
            if nodes_data[i] is None:
                nodes_data[i] = graph.Node(pos=graph.Position(), type="")

        self._decoding_graph = graph.BaseGraph(
            nodes=t.cast(list[graph.Node], nodes_data), edges=edges
        )
        self._edges_weights = np.array(edges_weights)

    @abc.abstractmethod
    def select_edges(
        self,
        syndrome: t.Sequence[bool],
        erased_nodes: t.Optional[t.Sequence[bool]] = None,
    ) -> t.Sequence[bool]:
        """Given a syndrome, return the selected edges indices given by the decoder.

        Args:
            syndrome: the computed syndrome to decode.
            erased_nodes: an array of booleans indicating which node at
                which round suffered erasure errors. ``None`` if the
                given decoder has no use for this.

        Returns:
            A list of bools, one per edge, indicating which was selected
            during decoding.

        Notes:
            Decoders must override this method in order to implement their logic. Each
            decoder will be given a syndrome, which is a set of vertices which have
            been "flipped", and erasure information, another set of vertices which
            have been "erased" across all rounds.
        """
        raise NotImplementedError

    def decode(
        self,
        syndrome: t.Sequence[bool],
        erased_nodes: t.Optional[t.Sequence[bool]] = None,
    ) -> pauli.Tableau:
        """Decode a given syndrome, calculating the most likely correction operator.

        Args:
            syndrome: the computed syndrome to decode.
            erased_nodes: an array of booleans indicating which node at
                which round suffered erasure errors.

        Returns:
            an operator that, when applied to the state of the system, should
            correct the errors detected by the code. The returned operator acts
            only on the **data** qubits of the state.

        See Also:
            :mod:`~plaquette.decoders` for an explanation of what type of
            syndrome and erasure information is expected here.
        """
        # Before doing anything, the syndrome that internally we deal with is
        # different from the one used by decoders. Then one returned by a Device does
        # not have any information about virtual edges, so we need to pad it
        # appropriately at each round
        assert (len(syndrome) // self._code.num_stabilizers) == self._n_rounds, (
            f"wrong number of syndrome bits ({len(syndrome)}) for the given code "
            f"you want to correct and given rounds ({self._n_rounds})"
        )
        # fmt: off
        syndrome = np.append(
            np.array(syndrome, dtype=int).reshape((self._n_rounds, self._code.num_stabilizers)), # noqa: E501
            np.zeros((self._n_rounds, len(self._virtual_ancillas) // self._n_rounds), dtype=int),  # noqa: E501
            axis=1
        ).ravel()
        # fmt: on

        # Next convert erased_nodes list into list of edges where erasures occured.
        # erased_node lists which data qubits were erased in each round.
        # The first n_qubits entries refer to the first round, the next
        # n_qubits entries to the second, etc.
        # The new erasure array lists edges . The first n_qubits entries
        # refer to X edges, the next n_qubits refer to Z, then X and Z again
        # followed by n_stabilizer edges referring to time-like edges, which cannot
        # have erasures.

        erasure = np.zeros_like(self._edges_weights, dtype=bool)

        if erased_nodes is not None:
            # Assuming the edges are listed according to X, Z, X, Z, I, X, Z, I, ...
            idx_in = 0  # index looping over the input list (erased_nodes)
            idx_out = 0  # index looping over output list (erasure)
            n_qubits = self._code.num_data_qubits

            # First round of erased qubits entries repeated twice: [X, Z]
            erasure[idx_out : idx_out + 2 * n_qubits] = np.tile(
                erased_nodes[idx_in : idx_in + n_qubits], 2
            )
            idx_in += n_qubits
            idx_out += 2 * n_qubits

            # Repeat (n_rounds-1) times [X, Z, I]
            for _ in range(self._n_rounds - 1):
                # Next n_qubits entries repeated twice
                erasure[idx_out : idx_out + 2 * n_qubits] = np.tile(
                    erased_nodes[idx_in : idx_in + n_qubits], 2
                )
                idx_in += n_qubits
                idx_out += 2 * n_qubits

                # Append n_stabilizers zeros for measurement-edges
                erasure[idx_out : idx_out + self._code.num_stabilizers] = 0
                idx_out += self._code.num_stabilizers

        # This completes conversion from `erased_nodes` to erased edges `erasure`

        # for each round of measurements, we need to XOR whatever edge was selected
        # at round r with the result at round r+1. This will give us the final
        # list of error mechanisms that we need to correct.
        # TODO: maybe this needs better explaining?
        errors = np.zeros(2 * self._code.num_data_qubits, dtype=int)

        # Cache erasure and syndrome to be able to dump them with the JSON file
        self._last_decoded_syndrome = syndrome
        self._last_decoded_erasure = t.cast(t.Sequence[bool], erasure)

        self.selection = np.flatnonzero(self.select_edges(syndrome, erasure))
        for edge in t.cast(t.Sequence[EdgeIndex], self.selection):
            edge_data = self._decoding_graph.edges[edge]
            assert edge_data is not None, "edge data missing"
            match edge_data.type:
                case pauli.Factor.I.name:
                    # Nothing to do for measurement edges
                    pass
                case pauli.Factor.X.name:
                    errors[self._data_qubit_index_for_edge[edge]] += 1
                case pauli.Factor.Z.name:
                    errors[
                        self._data_qubit_index_for_edge[edge]
                        + self._code.num_data_qubits
                    ] += 1
                case pauli.Factor.Y.name:
                    raise RuntimeError(
                        "encountered Y error in decoder correction, which "
                        "should not happen. This is probably a bug and should be "
                        "reported!"
                    )
                case other_string:
                    raise ValueError(
                        f"Edge of type `{other_string}` cannot be used for a "
                        "correction operator."
                    )

        return t.cast(pauli.Tableau, np.append(errors % 2, [0]).astype("u1"))  # adds a

    def results_to_json(self, file_name: pathlib.Path | str):
        """Save a JSON representation of this decoding graph.

        In the same folder as the one where the given ``file_name``
        lives, a new ``schema.json`` will be written. This is the
        JSON schema of the general graph JSON file that the visualiser
        expects.

        Args:
            file_name: file where to store the graph. If it exists, it
                will be overwritten without warning!
        """
        file_name = pathlib.Path(file_name).absolute()
        dec_graph = graph.DecodingGraph(
            nodes=self._decoding_graph.nodes,
            edges=self._decoding_graph.edges,
            selection=list(self.selection),
            faults=list(),
            virtual_nodes=self._virtual_ancillas,
            weights=self._edges_weights,
            logical_surfaces=[],
            # The two comprehensions are to satisfy mypy
            erasure=[i for i in np.flatnonzero(self._last_decoded_erasure)],
            syndrome=[i for i in np.flatnonzero(self._last_decoded_syndrome)],
        )
        file_name.write_text(dec_graph.model_dump_json())


class FusionBlossomDecoder(AbstractDecoder):
    """An interface to the ``fusion-blossom`` library decoder.

    See Also:
        https://github.com/yuewuo/fusion-blossom
    """

    def __init__(self, code: codes.Code, error_data: errors.ErrorDataDict, n_rounds=1):
        """Initialize a ``SolverSerial`` for decoding with ``fusion-blossom``."""
        super().__init__(code, error_data, n_rounds)
        # rescale weights and turn them into ints
        self._edges_weights[self._edges_weights == np.inf] = 2**24 - 1
        w = (1e5 * self._edges_weights / np.max(self._edges_weights)).astype(int)
        w[w == 0] = 1
        edges: list[tuple[NodeIndex, NodeIndex, int]] = list()
        for e_idx, edge in enumerate(self._decoding_graph.edges):
            if edge.a in self._virtual_ancillas and edge.b in self._virtual_ancillas:
                # We skip time-like indices for virtual ancillas
                continue
            edges.append(
                (
                    t.cast(NodeIndex, edge.a),
                    t.cast(NodeIndex, edge.b),
                    t.cast(int, 2 * w[e_idx]),
                )
            )
        self._solver = fb.SolverSerial(
            fb.SolverInitializer(
                len(self._decoding_graph.nodes), edges, self._virtual_ancillas
            )
        )

    def select_edges(
        self,
        syndrome: t.Sequence[bool],
        erased_edges: t.Optional[t.Sequence[bool]] = None,
    ) -> t.Sequence[bool]:
        """Return an edge selection after creating a ``SyndromePattern``."""
        pattern = fb.SyndromePattern(
            syndrome_vertices=np.flatnonzero(syndrome),
            erasures=np.flatnonzero(erased_edges) if erased_edges is not None else [],
        )
        self._solver.solve(pattern)
        selection = np.zeros(len(self._decoding_graph.edges), dtype=bool)
        selection[self._solver.subgraph(None)] = True
        self._solver.clear()
        return selection


class PyMatchingDecoder(AbstractDecoder):
    """An interface to the ``PyMatching`` (v2) decoder.

    See Also:
        https://github.com/oscarhiggott/PyMatching
    """

    def __init__(self, code: codes.Code, error_data: errors.ErrorDataDict, n_rounds=1):
        """Initialize a new PyMatching decoder instance."""
        super().__init__(code, error_data, n_rounds)
        # Before starting, PyMatching does not like infinite weights,
        # so we need to replace them with the maximum allowed value
        self._edges_weights[self._edges_weights == np.inf] = 2**24 - 1
        # Initialise empty decoder
        self._pym = pymatching.Matching()
        # Copy our graph structure into pymatching
        for e_idx, edge in enumerate(self._decoding_graph.edges):
            if edge.a in self._virtual_ancillas and edge.b in self._virtual_ancillas:
                # We ignore time-like edges for virtual ancillas, they will never
                # have errors
                continue
            self._pym.add_edge(
                edge.a, edge.b, fault_ids=e_idx, weight=self._edges_weights[e_idx]
            )

            # PyMatching concept of boundary edges is different from ours
            # if a not in self._virtual_ancillas and b not in self._virtual_ancillas:
            #     self._pym.add_edge(a, b)
            # elif a in self._virtual_ancillas:
            #     self._pym.add_boundary_edge(a)
            # else:
            #     self._pym.add_boundary_edge(b)
        self._pym.set_boundary_nodes(set(self._virtual_ancillas))

    def select_edges(
        self,
        syndrome: t.Sequence[bool],
        erased_edges: t.Optional[t.Sequence[bool]] = None,
    ) -> t.Sequence[bool]:
        """Return an array stating which edge was selected by PyMatching."""
        if erased_edges is not None:
            warnings.warn("pymatching decoder does not use erasure", stacklevel=2)
        return self._pym.decode(syndrome)
