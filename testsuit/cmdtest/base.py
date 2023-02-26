#!/usr/bin/env/python3
"""
Copyright 2023, Leon Freist
Author: Leon Freist <freist@informatik.uni-freiburg.de>

Written in the scope of Leon Freists Bachelor Thesis "x-search - A C++ Library for fast external String Search"
available at "https://github.com/lfreist/x-search"

testsuit is a collection of classes that can be used to test executables by comparing their output to a reference.
"""

import shutil
from typing import List
import subprocess

# ===== Helper functions ===============================================================================================

SILENT: bool = True


def log(*args, **kwargs):
    """
    Forward arguments to print() if SILENT is False.
    :param args:
    :param kwargs:
    :return:
    """
    if not SILENT:
        print(80 * " ", end='\r', flush=True)
        print(*args, **kwargs)


# ===== Base classes ===================================================================================================

class CommandResult:
    def __init__(self, command, passed: bool = False):
        self.command = command
        self.passed = passed

    def __bool__(self):
        return self.passed

    def __str__(self):
        return "passed" if self.passed else "failed"


class Command:
    """
    Base class of a command. Represents a single command together with a user chosen name describing the command
    """

    def __init__(self, name: str, cmd: List[str] | str):
        self.name = name
        self.cmd = cmd

    def __str__(self):
        if type(self.cmd) == str:
            return f"{self.name}: {self.cmd}"
        return f"{self.name}: {' '.join(self.cmd)}"

    def exists(self) -> bool:
        return shutil.which(self._get_binary_name()) is not None

    def _get_binary_name(self) -> str:
        if type(self.cmd) == str:
            return self.cmd.split(' ')[0]
        return self.cmd[0]

    def run(self) -> str:
        return subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                shell=(type(self.cmd) == str)).communicate()[0].decode()

    def run_compare(self, reference_command) -> CommandResult:
        out = subprocess.Popen(self.cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                               shell=(type(self.cmd) == str)).communicate()[0]
        return CommandResult(self, reference_command == out.decode())


class ReferenceCommand(Command):
    def __init__(self, name: str, cmd: List[str] | str):
        Command.__init__(self, name, cmd)
        self.output: str = ""

    def initialize(self):
        self.output = self.run()

    def __eq__(self, other: str):
        return self.output == other


class TestResult:
    def __init__(self, test_name: str):
        self.test_name = test_name
        self.results: dict = {}

    def __iadd__(self, other: CommandResult):
        self.results[other.command.name] = other
        return self

    def __bool__(self):
        """
        Returns whether all tests passed
        :return:
        """
        for _, res in self.results.items():
            if not bool(res):
                return False
        return True

    def __str__(self):
        passed = bool(self)
        if passed:
            return f"✅  {self.test_name}: PASSED"
        else:
            return f"❌  {self.test_name}: FAILED"

    def get_result(self) -> dict:
        return self.results


class TestSuit:
    def __init__(self, name: str, commands: List[Command], reference_command: ReferenceCommand,
                 setup_commands: List[Command] = None,
                 cleanup_commands: List[Command] = None, exit_on_fail: bool = False):
        self.name = name
        self.commands = commands
        self.reference_command = reference_command
        self.reference_command.initialize()
        self.setup_commands = setup_commands if setup_commands is not None else []
        self.cleanup_commands = cleanup_commands if cleanup_commands is not None else []
        self.exit_on_fail = exit_on_fail

    def __str__(self):
        return self.name

    def _setup(self):
        log("  ⏳ Setting things up...")
        for cmd in self.setup_commands:
            cmd.run()
        log("  ✅ Setup done")

    def _cleanup(self):
        log("  ⏳ Cleaning...")
        for cmd in self.cleanup_commands:
            cmd.run()
        log("  ✅ Cleanup done")

    def run(self) -> TestResult:
        self._setup()
        result = TestResult(self.name)
        for cmd in self.commands:
            res = cmd.run_compare(self.reference_command)
            if not res and self.exit_on_fail:
                raise TestFailedError(f"Test {result.test_name!r} failed.")
            result += res
        self._cleanup()
        return result


# ===== Error definitions ==============================================================================================

class TestFailedError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
