import cirq

import cirq_superstaq as css


def barrier_test() -> None:
    n = 3
    qubits = cirq.LineQubit.range(n)
    barrier = css.barrier(*qubits)
    assert barrier == css.Barrier(n).on(*cirq.LineQubit.range(n))
