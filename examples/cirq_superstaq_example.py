"""Creates and simulates a simple circuit generating a Bell state.

=== EXAMPLE OUTPUT ===
Circuit:
0: ---H(0)---@---M('output')---
             |
1: ----------X-----------------

Results:
output=1100011010111001...1101 (i.e., `job.counts()` returns {'0': 45, '1': 55})
"""

import cirq

import cirq_superstaq

# Creates Service class (used to create and run jobs) with api_key. Use API-generated superstaq
# token for api_key.
service = cirq_superstaq.Service(
    api_key="""Insert superstaq token that you received from https://superstaq.super.tech""",
    verbose=True,
)

# Create standard Bell circuit.
q0 = cirq.LineQubit(0)
q1 = cirq.LineQubit(1)
circuit = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1), cirq.measure(q0))

# Creating job with Service object.
job = service.create_job(circuit=circuit, repetitions=100, target="ibmq_qasm_simulator")

print("This is the job that's created: ", job.status())

# Get counts of the resultant job.
print(job.counts())
