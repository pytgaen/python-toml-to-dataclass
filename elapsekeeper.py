import time
from collections import defaultdict
from contextlib import ContextDecorator
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, Union, List, Dict


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


@dataclass()
class Elapsed:
    message_marker: Optional[str] = field(default=None)
    _start: float = field(default=None, init=False)  # , repr=False)
    _stop: Optional[float] = field(default=None, init=False)  # , repr=False)

    def __post_init__(self):
        self._start = time.perf_counter_ns()

    def stop(self) -> float:
        self._stop = time.perf_counter_ns()

    @property
    def elapse(self):
        return (self._stop - self._start) / 1_000_000_000


@dataclass
class TurnsElapsed:
    group_name: Optional[str] = None
    turns: List[Elapsed] = field(default_factory=list, init=False, repr=False)
    current_turn: Optional[Elapsed] = field(default=None, init=False, repr=False)

    def start(self, message_marker: Optional[str] = None) -> "TurnsElapsed":
        self.current_turn = Elapsed(message_marker)
        self.current_turn
        return self

    def turn(self, message_marker: Optional[str] = None) -> None:
        self.current_turn.stop()
        self.turns.append(self.current_turn)
        self.current_turn = Elapsed(message_marker)

    def stop(self) -> None:
        self.current_turn.stop()
        self.turns.append(self.current_turn)
        self.current_turn = None

    @property
    def cumul_elapse(self):
        return sum(t.elapse for t in self.turns)

    @property
    def mean_turn_elapse(self):
        return self.cumul_elapse / len(self.turns)

    @property
    def range_elapse(self):
        return self.turns[-1].stop - self.turns[0].start if self.turns else -1

    def summary(self) -> str:
        if len(self.turns) == 1:
            return f"{self.group_name} {self.cumul_elapse:0.4f} seconds\n"
        else:
            return f"{self.group_name} {self.cumul_elapse:0.4f} seconds; mean: {self.mean_turn_elapse:0.4f} seconds on {len(self.turns)} turns\n"

    def details(self) -> str:
        since_start = 0
        res = ""
        for t in self.turns:
            since_start += t.elapse
            res += f"{self.group_name} {t.message_marker} elapse {t.elapse:0.4f} seconds; since start {since_start:0.4f} seconds\n"

        return res


@dataclass
class ElapseKeeper(ContextDecorator):
    _groups_elapse: Optional[Dict[str, TurnsElapsed]] = field(default_factory=defaultdict, init=False, repr=False)

    message: Union[str, Callable[[float], str]] = "Elapsed time: {:0.4f} seconds"
    logger: Optional[Callable[[str], None]] = print

    def start(self, group_name: str = "__global__", message_marker: Optional[str] = None) -> None:
        self._groups_elapse[group_name] = TurnsElapsed(group_name).start(message_marker)

    def turn(self, group_name: str = "__global__", message_marker: Optional[str] = None) -> None:
        self._groups_elapse[group_name].turn(message_marker)

    def stop(self, group_name: str = "__global__") -> None:
        self._groups_elapse[group_name].stop()

    def summary(self) -> str:
        return [v_g.summary() for k_g, v_g in self._groups_elapse.items()]

    def details(self) -> str:
        return [v_g.details() for k_g, v_g in self._groups_elapse.items()]

    def _old_truc(self):
        if self.logger:
            if callable(self.text):
                text = self.text(self.last)
            else:
                attributes = {
                    "name": self.name,
                    "milliseconds": self.last * 1000,
                    "seconds": self.last,
                    "minutes": self.last / 60,
                }
                text = self.text.format(self.last, **attributes)
            self.logger(text)
        if self.name:
            self.timers.add(self.name, self.last)

        return self.last

    def __enter__(self) -> "ElapseKeeper":
        self.start("__global__")
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self.stop("__global__")
