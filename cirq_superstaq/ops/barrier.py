from typing import Tuple

import cirq

import cirq_superstaq as css


def barrier(*qubits: Tuple[cirq.Qid]) -> cirq.Operation:
    return css.Barrier(len(qubits)).on(*qubits)
