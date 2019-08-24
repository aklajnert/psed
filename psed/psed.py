# -*- coding: utf-8 -*-
import os
import sys
import typing

from psed.logger import Logger


class Psed:
    """Main class for psed"""

    def __init__(
        self,
        input: str = "",
        find: typing.List[str] = None,
        replace: str = "",
        inplace: bool = False,
    ):
        self.input: str = input
        self.find: typing.List[str] = find or []
        self.replace: str = replace
        self.in_place: bool = inplace

    def run(self):
        if not os.path.exists(self.input):
            sys.exit(f"Input not found in path: '{self.input}'")
