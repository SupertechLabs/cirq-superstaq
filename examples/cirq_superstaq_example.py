import cirq

import cirq_superstaq


q0 = cirq.LineQubit(0)
q1 = cirq.LineQubit(1)

circuit = cirq.Circuit(cirq.H(q0), cirq.measure(q0))


service = cirq_superstaq.Service(
    remote_host="https://127.0.0.1:5000",
    api_key="""ya29.a0ARrdaM9QJqCLZdNpNu9MY_m1WX6GhtyomBER7bANveiV_ZKsMYYFXmoTHC7bRhmnls91nhnrMQt5NE77xf04fqyF6hxmvHpZQMf9PfVsHReujINKQJJ-El_Xtzc_aCNvjprlfcZtYMXbSHdQc6FbzbilnpLp6A""",
    verbose=True,
)


# job = service.create_job(circuit=circuit, repetitions=1, target="azure_ionq_sim")
# print("This is the job that's created ", job.status())


job = service.qscout_compile(circuit)
print("This is the job that's created ", job)

