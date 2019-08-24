# -*- coding: utf-8 -*-
import glob
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
        input_ = self._get_input()

    def _get_input(self) -> typing.List[str]:
        if not os.path.exists(self.input):
            glob_input = glob.glob(self.input)
            if glob_input:
                Logger.log("Glob has matched following files:", 1)
                for item in glob_input:
                    Logger.log(f"\t- {item}", 1)
                return glob_input
            sys.exit(f"The input path doesn't exist: '{self.input}'")
        elif os.path.isfile(self.input):
            Logger.log(f"Found the input file: {self.input}")
            return [self.input]
        else:
            matches = []
            for root, dirnames, filenames in os.walk(self.input):
                for filename in filenames:
                    matches.append(os.path.join(root, filename))
            if not matches:
                sys.exit(f"Input directory: '{self.input}' contains no files.")
            Logger.log(f"Found {len(matches)} files in '{self.input}' directory:")
            for item in matches:
                Logger.log(f"\t- {item}", 1)
            return matches
