#
# This file is part of the linuxpy project
#
# Copyright (c) 2023 Tiago Coutinho
# Distributed under the GPLv3 license. See LICENSE for more info.

import os
import pathlib

from linuxpy.util import make_find

from .magic import Magic
from .statfs import get_fs_type
from .types import Optional, Iterable

MAGIC = Magic.SYSFS

MOUNT_PATH = pathlib.Path("/sys")
DEVICE_PATH = MOUNT_PATH / "bus/usb/devices"


def is_sysfs(path) -> bool:
    return get_fs_type(path) == MAGIC


def is_available() -> bool:
    return is_sysfs(MOUNT_PATH)


def iter_read_uevent(path: os.PathLike):
    path = pathlib.Path(path)
    with path.open() as f:
        for line in f:
            yield line.strip().split("=", 1)


class Device:
    syspath: pathlib.Path
    _subsystem: Optional[str] = None
    _attrs: Optional[dict] = None

    def __init__(self, syspath: os.PathLike):
        self.syspath = pathlib.Path(syspath)

    @classmethod
    def from_syspath(cls, syspath):
        syspath = pathlib.Path(syspath)
        if not syspath.exists():
            raise ValueError("Unknown syspath")
        syspath = syspath.resolve()
        return cls(syspath)

    @property
    def subsystem(self):
        if self._subsystem is None:
            self._subsystem = (self.syspath / "subsystem").resolve().stem
        return self._subsystem

    @property
    def attrs(self) -> dict[str, str]:
        if self._attrs is None:
            self._attrs = dict(iter_read_uevent(self.syspath / "uevent"))
        return self._attrs

    @property
    def devnum(self) -> int:
        return (int(self.attrs["MAJOR"]) << 8) + int(self.attrs["MINOR"])

    @property
    def devpath(self) -> pathlib.Path:
        return self.syspath

    @property
    def devname(self) -> str:
        return self.attrs.get("DEVNAME", "")


def iter_device_paths() -> Iterable[pathlib.Path]:
    char = MOUNT_PATH / "dev" / "char"
    block = MOUNT_PATH / "dev" / "block"
    yield from char.iterdir()
    yield from block.iterdir()


def iter_devices() -> Iterable[Device]:
    return (Device.from_syspath(path) for path in iter_device_paths())


find = make_find(iter_devices)


def main():
    devs = find(find_all=True)
    devs = sorted(devs, key=lambda dev: dev.subsystem)
    for dev in devs:
        major_minor = f"{dev.attrs['MAJOR']:>3}:{dev.attrs['MINOR']:<3}"
        print(f"{dev.devname:<20} {dev.subsystem:<16} {major_minor:<7} ({dev.devnum:>6}) {dev.syspath}")


if __name__ == "__main__":
    main()