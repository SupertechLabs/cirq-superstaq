"""Integration checks that run daily (via Github action) between client and prod server."""

import os

import cirq
import numpy as np
import pytest

import cirq_superstaq


@pytest.fixture
def service() -> cirq_superstaq.Service:
    token = os.getenv("TEST_USER_TOKEN")
    service = cirq_superstaq.Service(api_key=token)
    return service


def test_aqt_compile(service: cirq_superstaq.Service) -> None:
    qubits = cirq.LineQubit.range(8)
    circuit = cirq.Circuit(cirq.H(qubits[4]))
    expected = cirq.Circuit(
        cirq.rz(np.pi / 2)(qubits[4]),
        cirq.rx(np.pi / 2)(qubits[4]),
        cirq.rz(np.pi / 2)(qubits[4]),
    )
    assert service.aqt_compile(circuit).circuit == expected
    assert service.aqt_compile([circuit]).circuits == [expected]
    assert service.aqt_compile([circuit, circuit]).circuits == [expected, expected]


def test_get_balance(service: cirq_superstaq.Service) -> None:
    assert isinstance(service.get_balance(pretty_output=False), float)


def test_tsp(service: cirq_superstaq.Service) -> None:
    cities = ["Chicago", "San Francisco", "New York City", "New Orleans"]
    out = service.tsp(cities)
    for city in cities:
        assert city.replace(" ", "+") in out.map_link[0]


def test_get_backends(service: cirq_superstaq.Service) -> None:
    expected = {
        "compile-and-run": [
            "ibmq_qasm_simulator",
            "ibmq_armonk_qpu",
            "ibmq_santiago_qpu",
            "ibmq_bogota_qpu",
            "ibmq_lima_qpu",
            "ibmq_belem_qpu",
            "ibmq_quito_qpu",
            "ibmq_statevector_simulator",
            "ibmq_mps_simulator",
            "ibmq_extended-stabilizer_simulator",
            "ibmq_stabilizer_simulator",
            "ibmq_manila_qpu",
            "aws_dm1_simulator",
            "aws_sv1_simulator",
            "d-wave_advantage-system4.1_qpu",
            "d-wave_dw-2000q-6_qpu",
            "aws_tn1_simulator",
            "rigetti_aspen-9_qpu",
            "d-wave_advantage-system1.1_qpu",
            "ionq_ion_qpu",
        ],
        "compile-only": ["aqt_keysight_qpu", "sandia_qscout_qpu"],
    }
    assert service.get_backends() == expected
