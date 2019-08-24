# -*- coding: utf-8 -*-
import glob
import os
import re
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
        self.find: typing.List[typing.Pattern] = self._get_patterns(find)
        self.replace: str = replace
        self.in_place: bool = inplace

    def run(self):
        input_list = self._get_input()

        match = any(bool(self.process_file(item)) for item in input_list)
        if not match:
            Logger.log("No matches.")

    def process_file(self, path: str):
        with open(path) as file_handle:
            try:
                content = file_handle.read()
            except UnicodeDecodeError:  # pragma: no cover
                Logger.log(f"File is binary: {path}", 2)
                return []

        if not self.replace:
            return self._find_only(content, path)

    def _find_only(self, content, path):
        matches = []
        for pattern in self.find:
            pattern_matches = (match for match in pattern.finditer(content))
            if pattern_matches:
                matches.extend(pattern_matches)
        if matches:
            Logger.log(
                f"{path}: {len(matches)} {'matches' if len(matches) > 1 else 'match'}:"
            )
            for match in matches:
                Logger.log(f"\t{match.span()}: {match.group()}")
        return matches

    def _get_patterns(self, patterns) -> typing.List[typing.Pattern]:
        if patterns is None:
            return []
        output = []
        failures = False
        for pattern in patterns:
            try:
                output.append(re.compile(pattern))
            except re.error as exc:
                Logger.log(f"Cannot compile pattern: {pattern}\n\t{exc}", -1)
                failures = True
        if failures:
            sys.exit("Some find patterns have no been compiled successfully.")
        return output

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
