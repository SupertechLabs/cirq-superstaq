"""Miscellaneous custom gates that we encounter and want to explicitly define."""

from typing import Any, Callable, Dict, List, Sequence, Tuple, Union

import cirq
import numpy as np

import cirq_superstaq


@cirq.value_equality(approximate=True)
class FermionicSWAPGate(
    cirq.ops.gate_features.TwoQubitGate, cirq.ops.gate_features.InterchangeableQubitsGate
):
    r"""The Fermionic SWAP gate, which performs the ZZ-interaction followed by a SWAP.

    Fermionic SWAPs are useful for applications like QAOA or Hamiltonian Simulation,
    particularly on linear- or low- connectivity devices. See https://arxiv.org/pdf/2004.14970.pdf
    for an application of Fermionic SWAP networks.

    The unitary for a Fermionic SWAP gate parametrized by ZZ-interaction angle :math:`\theta` is:

     .. math::

        \begin{bmatrix}
        1 & . & . & . \\
        . & . & e^{i \theta} & . \\
        . & e^{i \theta} & . & . \\
        . & . & . & 1 \\
        \end{bmatrix}

    where '.' means '0'.
    For :math:`\theta = 0`, the Fermionic SWAP gate is just an ordinary SWAP.

    Note that this gate is NOT the same as ``cirq.FSimGate``.
    """

    def __init__(self, theta: float) -> None:
        """
        Args:
            theta: ZZ-interaction angle in radians
        """
        self.theta = cirq.ops.fsim_gate._canonicalize(theta)  # between -pi and +pi

    def _unitary_(self) -> np.ndarray:
        return np.array(
            [
                [1, 0, 0, 0],
                [0, 0, np.exp(1j * self.theta), 0],
                [0, np.exp(1j * self.theta), 0, 0],
                [0, 0, 0, 1],
            ]
        )

    def _value_equality_values_(self) -> Any:
        return self.theta

    def __str__(self) -> str:
        return f"FermionicSWAPGate({self.theta})"

    def __repr__(self) -> str:
        return f"cirq_superstaq.custom_gates.FermionicSWAPGate({self.theta})"

    def _circuit_diagram_info_(self, args: cirq.CircuitDiagramInfoArgs) -> cirq.CircuitDiagramInfo:
        t = args.format_radians(self.theta)
        return cirq.CircuitDiagramInfo(wire_symbols=(f"FermionicSWAP({t})", f"FermionicSWAP({t})"))

    def _json_dict_(self) -> Dict[str, Any]:
        return cirq.protocols.obj_to_dict_helper(self, ["theta"])


class ZXPowGate(cirq.EigenGate, cirq.TwoQubitGate):
    r"""The ZX-parity gate, possibly raised to a power.
    Per arxiv.org/pdf/1904.06560v3 eq. 135, the ZX**t gate implements the following unitary:
     .. math::
        e^{-\frac{i}{2} Z \otimes X} = \begin{bmatrix}
                                        c & -s & . & . \\
                                        -s & c & . & . \\
                                        . & . & c & s \\
                                        . & . & s & c \\
                                        \end{bmatrix}
    where '.' means '0' and :math:`c = \cos(\frac{\pi t}{2})`
    and :math:`s = i \sin(\frac{\pi t}{2})`.
    """

    def _eigen_components(self) -> List[Tuple[float, np.ndarray]]:
        return [
            (
                0.0,
                np.array(
                    [[0.5, 0.5, 0, 0], [0.5, 0.5, 0, 0], [0, 0, 0.5, -0.5], [0, 0, -0.5, 0.5]]
                ),
            ),
            (
                1.0,
                np.array(
                    [[0.5, -0.5, 0, 0], [-0.5, 0.5, 0, 0], [0, 0, 0.5, 0.5], [0, 0, 0.5, 0.5]]
                ),
            ),
        ]

    def _eigen_shifts(self) -> List[float]:
        return [0, 1]

    def _circuit_diagram_info_(
        self, args: cirq.CircuitDiagramInfoArgs
    ) -> cirq.protocols.CircuitDiagramInfo:
        return cirq.protocols.CircuitDiagramInfo(
            wire_symbols=("Z", "X"), exponent=self._diagram_exponent(args)
        )

    def __str__(self) -> str:
        if self.exponent == 1:
            return "ZX"
        return f"ZX**{self._exponent!r}"

    def __repr__(self) -> str:
        if self._global_shift == 0:
            if self._exponent == 1:
                return "cirq_superstaq.ZX"
            return f"(cirq_superstaq.ZX**{cirq._compat.proper_repr(self._exponent)})"
        return (
            f"cirq_superstaq.ZXPowGate(exponent={cirq._compat.proper_repr(self._exponent)},"
            f" global_shift={self._global_shift!r})"
        )


CR = ZX = ZXPowGate()  # standard CR is a full turn of ZX, i.e. theta = 180
CR45P = CR ** 0.25
CR45N = CR ** -0.25


class aceCR(cirq.TwoQubitGate):
    def __init__(self, polarity: str) -> None:
        assert polarity in ["+-", "-+"]
        self.polarity = polarity
        super().__init__()

    def _decompose_(self, qubits: Tuple[cirq.LineQubit, cirq.LineQubit]) -> cirq.OP_TREE:
        yield cirq_superstaq.CR45P(*qubits) if self.polarity == "+-" else cirq_superstaq.CR45N(
            *qubits
        )
        yield cirq.X(qubits[0])
        yield cirq_superstaq.CR45N(*qubits) if self.polarity == "+-" else cirq_superstaq.CR45P(
            *qubits
        )

    def _circuit_diagram_info_(
        self, args: cirq.CircuitDiagramInfoArgs
    ) -> cirq.protocols.CircuitDiagramInfo:
        return cirq.protocols.CircuitDiagramInfo(
            wire_symbols=(f"aceCR{self.polarity}(Z side)", f"aceCR{self.polarity}(X side)")
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, aceCR):
            return False
        return self.polarity == other.polarity

    def __hash__(self) -> int:
        return hash(self.polarity)

    def __repr__(self) -> str:
        return f"cirq_superstaq.aceCR('{self.polarity}')"

    def __str__(self) -> str:
        return f"aceCR{self.polarity}"


class aceCRMinusPlus(aceCR):
    def __init__(self) -> None:
        super().__init__("-+")

    # def _decompose_(self, qubits: Tuple[cirq.LineQubit, cirq.LineQubit]) -> cirq.OP_TREE:
    #     yield cirq_superstaq.CR45N(
    #         *qubits
    #     )
    #     yield cirq.X(qubits[0])
    #     yield cirq_superstaq.CR45P(
    #         *qubits
    #     )

    # def _circuit_diagram_info_(
    #     self, args: cirq.CircuitDiagramInfoArgs
    # ) -> cirq.protocols.CircuitDiagramInfo:
    #     return cirq.protocols.CircuitDiagramInfo(
    #         wire_symbols=(f"aceCR-+(Z side)", f"aceCR-+(X side)")
    #     )

    # def __eq__(self, other: object) -> bool:
    #     if not isinstance(other, aceCR):
    #         return False
    #     return self.polarity == other.polarity

    # def __hash__(self) -> int:
    #     return hash(self.polarity)

    # def __repr__(self) -> str:
    #     return f"cirq_superstaq.custom_gates.aceCRMinusPlus()"

    # def __str__(self) -> str:
    #     return f"aceCR-+"


class aceCRPlusMinus(aceCR):
    def __init__(self) -> None:
        super().__init__("+-")


class Barrier(cirq.ops.IdentityGate):
    """Barrier: temporal boundary restricting circuit compilation and pulse scheduling.
    Otherwise equivalent to the identity gate.
    """

    def _decompose_(self, qubits: Sequence["cirq.Qid"]) -> cirq.type_workarounds.NotImplementedType:
        return NotImplemented

    def _qasm_(self, args: cirq.QasmArgs, qubits: Tuple[cirq.Qid, ...]) -> str:
        indices_str = ",".join([f"{{{i}}}" for i in range(len(qubits))])
        format_str = f"barrier {indices_str};\n"
        return args.format(format_str, *qubits)

    def __str__(self) -> str:
        return f"Barrier({self.num_qubits()})"

    def __repr__(self) -> str:
        return f"cirq_superstaq.custom_gates.Barrier({self.num_qubits()})"

    def _circuit_diagram_info_(self, args: cirq.CircuitDiagramInfoArgs) -> Tuple[str, ...]:
        return ("|",) * self.num_qubits()


def custom_resolver(cirq_type: str) -> Union[Callable[..., cirq.Gate], None]:
    print(cirq_type)
    if cirq_type == "FermionicSWAPGate":
        return FermionicSWAPGate
    if cirq_type == "Barrier":
        return Barrier
    if cirq_type == "ZXPowGate":
        return ZXPowGate
    if cirq_type == "aceCRMinusPlus":
        return aceCRMinusPlus
    if cirq_type == "aceCRPlusMinus":
        return aceCRPlusMinus
    return None
