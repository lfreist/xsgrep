"""
Copyright 2023, Leon Freist
Author: Leon Freist <freist@informatik.uni-freiburg.de>

Test xsgrep by comparing its output to GNU grep
"""
import argparse
import os
import re
import subprocess
import sys

import requests
import base

INPUT_FILE = "en.txt"

ASCII_PATTERN = "Sherlock"

ASCII_RE = "She[r ]lock"

EXIT_ON_FAIL = False


def test_plain_ascii() -> base.TestSuit:
    ref_command = base.ReferenceCommand("grep", ["grep", ASCII_PATTERN, INPUT_FILE])
    commands = [
        base.Command("xs", ["xs", ASCII_PATTERN, INPUT_FILE]),
        base.Command("xs -j 1", ["xs", ASCII_PATTERN, INPUT_FILE, "-j", "1"]),
        base.Command("xs --no-mmap", ["xs", ASCII_PATTERN, INPUT_FILE, "--no-mmap"]),
    ]
    return base.TestSuit(
        "ASCII search",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_regex_ascii() -> base.TestSuit:
    ref_command = base.ReferenceCommand("grep", ["grep", ASCII_RE, INPUT_FILE])
    commands = [
        base.Command("xs", ["xs", ASCII_RE, INPUT_FILE]),
        base.Command("xs -j 1", ["xs", ASCII_RE, INPUT_FILE, "-j", "1"]),
        base.Command("xs --no-mmap", ["xs", ASCII_RE, INPUT_FILE, "--no-mmap"]),
    ]
    return base.TestSuit(
        "ASCII regex search",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_ascii_line_numbers() -> base.TestSuit:
    ref_command = base.ReferenceCommand("grep", ["grep", ASCII_PATTERN, INPUT_FILE, "-n"])
    commands = [
        base.Command("xs", ["xs", ASCII_PATTERN, INPUT_FILE, "-n"]),
        base.Command("xs -j 1", ["xs", ASCII_PATTERN, INPUT_FILE, "-j", "1", "-n"]),
        base.Command("xs --no-mmap", ["xs", ASCII_PATTERN, INPUT_FILE, "-n", "--no-mmap"]),
    ]
    return base.TestSuit(
        "ASCII search (-n)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_regex_ascii_line_numbers() -> base.TestSuit:
    ref_command = base.ReferenceCommand("grep", ["grep", ASCII_RE, INPUT_FILE, "-n"])
    commands = [
        base.Command("xs", ["xs", ASCII_RE, INPUT_FILE, "-n"]),
        base.Command("xs -j 1", ["xs", ASCII_RE, INPUT_FILE, "-j", "1", "-n"]),
        base.Command("xs --no-mmap", ["xs", ASCII_RE, INPUT_FILE, "-n", "--no-mmap"]),
    ]
    return base.TestSuit(
        "ASCII regex search (-n)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_ascii_ignore_case() -> base.TestSuit:
    ref_command = base.ReferenceCommand("grep", ["grep", ASCII_PATTERN, INPUT_FILE, "-i"])
    commands = [
        base.Command("xs", ["xs", ASCII_PATTERN, INPUT_FILE, "-i"]),
        base.Command("xs -j 1", ["xs", ASCII_PATTERN, INPUT_FILE, "-j", "1", "-i"]),
        base.Command("xs --no-mmap", ["xs", ASCII_PATTERN, INPUT_FILE, "-i", "--no-mmap"]),
    ]
    return base.TestSuit(
        "ASCII search (-i)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_regex_ascii_ignore_case() -> base.TestSuit:
    ref_command = base.ReferenceCommand("grep", ["grep", ASCII_RE, INPUT_FILE, "-i"])
    commands = [
        base.Command("xs", ["xs", ASCII_RE, INPUT_FILE, "-i"]),
        base.Command("xs -j 1", ["xs", ASCII_RE, INPUT_FILE, "-j", "1", "-i"]),
        base.Command("xs --no-mmap", ["xs", ASCII_RE, INPUT_FILE, "-i", "--no-mmap"]),
    ]
    return base.TestSuit(
        "ASCII regex search (-i)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_ascii_byte_offsets() -> base.TestSuit:
    ref_command = base.ReferenceCommand("grep", ["grep", ASCII_PATTERN, INPUT_FILE, "-b"])
    commands = [
        base.Command("xs", ["xs", ASCII_PATTERN, INPUT_FILE, "-b"]),
        base.Command("xs -j 1", ["xs", ASCII_PATTERN, INPUT_FILE, "-j", "1", "-b"]),
        base.Command("xs --no-mmap", ["xs", ASCII_PATTERN, INPUT_FILE, "-b", "--no-mmap"]),
    ]
    return base.TestSuit(
        "ASCII search (-b)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_regex_ascii_byte_offsets() -> base.TestSuit:
    ref_command = base.ReferenceCommand("grep", ["grep", ASCII_RE, INPUT_FILE, "-b"])
    commands = [
        base.Command("xs", ["xs", ASCII_RE, INPUT_FILE, "-b"]),
        base.Command("xs -j 1", ["xs", ASCII_RE, INPUT_FILE, "-j", "1", "-b"]),
        base.Command("xs --no-mmap", ["xs", ASCII_RE, INPUT_FILE, "-b", "--no-mmap"]),
    ]
    return base.TestSuit(
        "ASCII regex search (-b)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_ascii_match_only() -> base.TestSuit:
    ref_command = base.ReferenceCommand("grep", ["grep", ASCII_PATTERN, INPUT_FILE, "-o"])
    commands = [
        base.Command("xs", ["xs", ASCII_PATTERN, INPUT_FILE, "-o"]),
        base.Command("xs -j 1", ["xs", ASCII_PATTERN, INPUT_FILE, "-j", "1", "-o"]),
        base.Command("xs --no-mmap", ["xs", ASCII_PATTERN, INPUT_FILE, "-o", "--no-mmap"]),
    ]
    return base.TestSuit(
        "ASCII search (-o)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_regex_ascii_match_only() -> base.TestSuit:
    ref_command = base.ReferenceCommand("grep", ["grep", ASCII_RE, INPUT_FILE, "-o"])
    commands = [
        base.Command("xs", ["xs", ASCII_RE, INPUT_FILE, "-o"]),
        base.Command("xs -j 1", ["xs", ASCII_RE, INPUT_FILE, "-j", "1", "-o"]),
        base.Command("xs --no-mmap", ["xs", ASCII_RE, INPUT_FILE, "-o", "--no-mmap"]),
    ]
    return base.TestSuit(
        "ASCII regex search (-o)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_ascii_fixed_string() -> base.TestSuit:
    ref_command = base.ReferenceCommand("grep", ["grep", ASCII_RE, INPUT_FILE, "-F"])
    commands = [
        base.Command("xs", ["xs", ASCII_RE, INPUT_FILE, "-F"]),
        base.Command("xs -j 1", ["xs", ASCII_RE, INPUT_FILE, "-j", "1", "-F"]),
        base.Command("xs --no-mmap", ["xs", ASCII_RE, INPUT_FILE, "-F", "--no-mmap"]),
    ]
    return base.TestSuit(
        "ASCII search (-F)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_count() -> base.TestSuit:
    pass


def parse_args():
    parser = argparse.ArgumentParser(prog="xs_test", description="Automated test of xs grep")
    parser.add_argument("input", metavar="INPUT_FILE", help="File to be searched")
    parser.add_argument("--list-benchmarks", action="store_true", help="List available benchmarks by name and exit")
    parser.add_argument("--exit-on-failure", action="store_true", help="Stop testing if a single test fails")
    parser.add_argument("--filter", metavar="FILTER", default="", help="Filter benchmarks by name using regex")
    parser.add_argument("--silent", action="store_true", help="Do not output log messages")

    return parser.parse_args()


if __name__ == "__main__":
    benchmarks = {
        "xsgrep plain ASCII": test_plain_ascii,
        "xsgrep regex ASCII": test_regex_ascii,
        "xsgrep plain ASCII (-b)": test_plain_ascii_byte_offsets,
        "xsgrep regex ASCII (-b)": test_regex_ascii_byte_offsets,
        "xsgrep plain ASCII (-n)": test_plain_ascii_line_numbers,
        "xsgrep regex ASCII (-n)": test_regex_ascii_line_numbers,
        "xsgrep plain ASCII (-f)": test_plain_ascii_fixed_string,
        "xsgrep plain ASCII (-i)": test_plain_ascii_ignore_case,
        "xsgrep regex ASCII (-i)": test_regex_ascii_ignore_case,
        "xsgrep plain ASCII (-o)": test_plain_ascii_match_only,
        "xsgrep regex ASCII (-o)": test_regex_ascii_match_only,
    }
    args = parse_args()
    EXIT_ON_FAIL = args.exit_on_failure
    INPUT_FILE = args.input
    base.SILENT = args.silent
    if args.list_benchmarks:
        print("The following benchmarks are available:")
        for name in benchmarks.keys():
            print(f" - {name}")
        exit(0)

    failed = 0
    run = 0
    for name, bm_func in benchmarks.items():
        res = None
        if re.search(args.filter, name):
            res = bm_func().run()
            if str(res).endswith("FAILED"):
                failed += 1
            run += 1
            print(res)

    print("================================================================================")
    if failed > 0:
        print(f"{failed} out of {run} tests failed.")
        sys.exit(1)
    else:
        print(f"All Tests ({run}) passed.")
