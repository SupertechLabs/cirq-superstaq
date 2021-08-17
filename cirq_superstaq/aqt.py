import codecs
import importlib
import pickle
from dataclasses import dataclass
from typing import Callable, List, Optional, Union

import cirq

try:
    import qtrl.sequencer
except ModuleNotFoundError:
    pass

PulseType = Union[
    List["qtrl.sequencer.UniquePulse"],
    Callable[[cirq.Operation], "qtrl.sequencer.Sequence"],
    "qtrl.sequencer.Sequence",
]


@dataclass
class AQTCompilerOutput:
    circuit: cirq.Circuit
    seq: Optional["qtrl.sequencer.Sequence"] = None
    pulse_list: Optional[List[List[PulseType]]] = None


def read_json(json_dict: dict) -> AQTCompilerOutput:
    """Reads out returned JSON from SuperstaQ API's AQT compilation endpoint.

    Args:
        json_dict: a JSON dictionary matching the format returned by /aqt_compile endpoint
    Returns:
        a AQTCompilerOutput object with the compiled circuit. If qtrl is available locally,
        the object also stores the pulse sequence in the .seq attribute and the pulse list
        in the .pulse_list attribute.
    """
    compiled_circuit = cirq.read_json(json_text=json_dict["compiled_circuit"])

    if not importlib.util.find_spec("qtrl"):
        return AQTCompilerOutput(compiled_circuit)

    else:  # pragma: no cover, b/c qtrl is not open source so it is not in cirq-superstaq reqs
        state_str = json_dict["state_jp"]
        state = pickle.loads(codecs.decode(state_str.encode(), "base64"))

        pulse_list_str = json_dict["pulse_list_jp"]
        pulse_list = pickle.loads(codecs.decode(pulse_list_str.encode(), "base64"))

        seq = qtrl.sequencer.Sequence(n_elements=1)
        seq.__setstate__(state)
        seq.compile()

        return AQTCompilerOutput(compiled_circuit, seq, pulse_list)
