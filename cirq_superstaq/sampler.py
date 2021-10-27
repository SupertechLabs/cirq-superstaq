# Copyright 2021 The Cirq Developers
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A `cirq.Sampler` implementation for the SuperstaQ API."""

from typing import List, Optional

import cirq

import cirq_superstaq


class Sampler(cirq.Sampler):
    """A sampler that works against the SuperstaQ API. Users should get a sampler from the `sampler`
    method on `cirq_superstaq.Service`.

    Example:

        >> service = cirq_superstaq.Service(...)
        >> q0, q1 = cirq.LineQubit.range(2)
        >> sampler = service.sampler()
        >> circuit = cirq.Circuit(cirq.H(q0), cirq.CNOT(q0, q1), cirq.measure(q0))
        >> print(sampler.sample(circuit, repetitions=5))
        out
        0   1
        1   1
        2   1
        3   1

    """

    def __init__(
        self,
        service: cirq_superstaq.Service,
        target: Optional[str],
    ):
        """Constructs the sampler. Uers should get a sampler from the `sampler` method on
        `cirq_superstaq.Service`.

        Args:
            service: The service used to create this sample.
            target: Backend on which to run the job.

        Returns:
            None.
        """
        self._service = service
        self._target = target

    def run_sweep(
        self,
        program: cirq.AbstractCircuit,
        params: cirq.Sweepable,
        repetitions: int = 1,
    ) -> List["cirq.Result"]:
        """Runs a sweep for the given Circuit. Note that this creates jobs for each of the sweeps in
        the given sweepable, and then blocks until all of jobs are complete.

        Ags:
            program: The circuit to sample from.
            params: The parameters to run with program.
            repetitions: The number of times to sample.

        Returns:
            A list of Cirq results, one for each parameter resolver.
        """
        resolvers = [resolver for resolver in cirq.to_resolvers(params)]
        jobs = [
            self._service.create_job(
                circuit=cirq.resolve_parameters(program, resolver),
                repetitions=repetitions,
                target=self._target,
            )
            for resolver in resolvers
        ]
        job_results = [job.results() for job in jobs]
        cirq_results = []
        for result, params in zip(job_results, resolvers):
            cirq_results.append(result.to_cirq_result(params=params))
        return cirq_results
