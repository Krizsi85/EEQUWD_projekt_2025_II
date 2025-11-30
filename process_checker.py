import psutil
import os
from enum import Enum, auto
from dataclasses import dataclass


class ProcessStatus(Enum):
    ONLINE = auto()
    OFFLINE = auto()
    MULTIPLE = auto()


@dataclass
class ProcessInfo:
    pid: int
    path: str
    start_time: float


class ProcessChecker:
    def __init__(self, exe_path):
        self.exe_path = os.path.abspath(exe_path)

    def check(self):
        found = []

        for p in psutil.process_iter(["pid", "exe", "create_time"]):
            try:
                exe = p.info["exe"]
                if exe and os.path.abspath(exe) == self.exe_path:
                    found.append(p)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        if len(found) == 0:
            return ProcessStatus.OFFLINE, None

        if len(found) > 1:
            return ProcessStatus.MULTIPLE, None

        proc = found[0]
        return ProcessStatus.ONLINE, ProcessInfo(
            pid=proc.pid,
            path=proc.info["exe"],
            start_time=proc.info["create_time"]
        )
