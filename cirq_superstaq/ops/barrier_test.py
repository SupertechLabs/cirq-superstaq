import cirq

import cirq_superstaq as css


def test_barrier() -> None:
    n = 3
    qubits = cirq.LineQubit.range(n)
    barrier = css.barrier(qubits)
    assert barrier == css.Barrier(n).on(*cirq.LineQubit.range(n))
