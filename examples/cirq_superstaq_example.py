import cirq

import cirq_superstaq

# Use API-generated superstaq token for api_key.
# Creates Service class (used to create and run jobs) with api_key.
service = cirq_superstaq.Service(api_key="""insert superstaq token""", verbose=True)

# Create standard bell circuit
q0 = cirq.LineQubit(0)
q1 = cirq.LineQubit(1)
circuit = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1), cirq.measure(q0))

# Creating job with Service object
job = service.create_job(circuit=circuit, repetitions=100, target="ibmq_qasm_simulator")

print("This is the job that's created: ", job.status())

# Get counts of the resultant job
print(job.counts())
