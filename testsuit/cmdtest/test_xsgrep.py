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

INPUT_FILE = "test/files/sample.txt"

ASCII_PATTERN = "Sherlock"

ASCII_RE = "She[r ]lock"

EXIT_ON_FAIL = False


def test_literal_ascii() -> base.TestSuit:
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


def test_literal_ascii_line_numbers() -> base.TestSuit:
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


def test_literal_ascii_ignore_case() -> base.TestSuit:
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


def test_literal_ascii_byte_offsets() -> base.TestSuit:
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


def test_literal_ascii_match_only() -> base.TestSuit:
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


def test_literal_ascii_fixed_string() -> base.TestSuit:
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


def test_preprocessed_regex() -> base.TestSuit:
    ref_command = base.ReferenceCommand("grep", ["grep", ASCII_RE, INPUT_FILE, "-n"])
    meta = "tmp.meta"
    lz4 = "xslz4"
    lz4_meta = "xslz4.meta"
    lz4hc = "xslz4hc"
    lz4hc_meta = "xslz4hc.meta"
    zst = "xszst"
    zst_meta = "xszst.meta"
    commands = [
        base.Command("xs", ["xs", ASCII_RE, INPUT_FILE, "-m", meta, "-n"]),
        base.Command("xs -j 1", ["xs", ASCII_RE, INPUT_FILE, "-j", "1", "-m", meta, "-n"]),
        base.Command("xs --max-readers 2", ["xs", ASCII_RE, INPUT_FILE, "--max-readers", "2", "-m", meta, "-n"]),
        base.Command("xs lz4", ["xs", ASCII_RE, lz4, "-m", lz4_meta, "-n"]),
        base.Command("xs -j 1 lz4", ["xs", ASCII_RE, lz4, "-j", "1", "-m", lz4_meta, "-n"]),
        base.Command("xs --max-readers 2 lz4", ["xs", ASCII_RE, lz4, "--max-readers", "2", "-m", lz4_meta, "-n"]),
        base.Command("xs lz4hc", ["xs", ASCII_RE, lz4hc, "-m", lz4hc_meta, "-n"]),
        base.Command("xs -j 1 lz4hc", ["xs", ASCII_RE, lz4hc, "-j", "1", "-m", lz4hc_meta, "-n"]),
        base.Command("xs --max-readers 2 lz4hc", ["xs", ASCII_RE, lz4hc, "--max-readers", "2", "-m", lz4hc_meta, "-n"]),
        base.Command("xs zst", ["xs", ASCII_RE, zst, "-m", zst_meta, "-n"]),
        base.Command("xs -j 1 zst", ["xs", ASCII_RE, zst, "-j", "1", "-m", zst_meta, "-n"]),
        base.Command("xs --max-readers 2 zst", ["xs", ASCII_RE, zst, "--max-readers", "2", "-m", zst_meta, "-n"]),
    ]
    return base.TestSuit(
        "Preprocessed regex search",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL,
        setup_commands=[
            base.Command("xspp meta", ["xspp", INPUT_FILE, "-m", meta]),
            base.Command("xspp lz4", ["xspp", INPUT_FILE, "-m", lz4_meta, "-o", lz4, "-a", "lz4"]),
            base.Command("xspp lz4hc", ["xspp", INPUT_FILE, "-m", lz4hc_meta, "-o", lz4hc, "-a", "lz4", "--hc"]),
            base.Command("xspp zst", ["xspp", INPUT_FILE, "-m", zst_meta, "-o", zst, "-a", "zstd"])
        ],
        cleanup_commands=[base.Command("rm", ["rm", meta, lz4, lz4_meta, lz4hc, lz4hc_meta, zst, zst_meta])]
    )


def test_preprocessed_literal() -> base.TestSuit:
    ref_command = base.ReferenceCommand("grep", ["grep", ASCII_PATTERN, INPUT_FILE, "-n"])
    meta = "tmp.meta"
    lz4 = "xslz4"
    lz4_meta = "xslz4.meta"
    lz4hc = "xslz4hc"
    lz4hc_meta = "xslz4hc.meta"
    zst = "xszst"
    zst_meta = "xszst.meta"
    commands = [
        base.Command("xs", ["xs", ASCII_PATTERN, INPUT_FILE, "-m", meta, "-n"]),
        base.Command("xs -j 1", ["xs", ASCII_PATTERN, INPUT_FILE, "-j", "1", "-m", meta, "-n"]),
        base.Command("xs --max-readers 2", ["xs", ASCII_PATTERN, INPUT_FILE, "--max-readers", "2", "-m", meta, "-n"]),
        base.Command("xs lz4", ["xs", ASCII_PATTERN, lz4, "-m", lz4_meta, "-n"]),
        base.Command("xs -j 1 lz4", ["xs", ASCII_PATTERN, lz4, "-j", "1", "-m", lz4_meta, "-n"]),
        base.Command("xs --max-readers 2 lz4", ["xs", ASCII_PATTERN, lz4, "--max-readers", "2", "-m", lz4_meta, "-n"]),
        base.Command("xs lz4hc", ["xs", ASCII_PATTERN, lz4hc, "-m", lz4hc_meta, "-n"]),
        base.Command("xs -j 1 lz4hc", ["xs", ASCII_PATTERN, lz4hc, "-j", "1", "-m", lz4hc_meta, "-n"]),
        base.Command("xs --max-readers 2 lz4hc", ["xs", ASCII_PATTERN, lz4hc, "--max-readers", "2", "-m", lz4hc_meta, "-n"]),
        base.Command("xs zst", ["xs", ASCII_PATTERN, zst, "-m", zst_meta, "-n"]),
        base.Command("xs -j 1 zst", ["xs", ASCII_PATTERN, zst, "-j", "1", "-m", zst_meta, "-n"]),
        base.Command("xs --max-readers 2 zst", ["xs", ASCII_PATTERN, zst, "--max-readers", "2", "-m", zst_meta, "-n"]),
    ]
    return base.TestSuit(
        "Preprocessed literal search",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL,
        setup_commands=[
            base.Command("xspp meta", ["xspp", INPUT_FILE, "-m", meta]),
            base.Command("xspp lz4", ["xspp", INPUT_FILE, "-m", lz4_meta, "-o", lz4, "-a", "lz4"]),
            base.Command("xspp lz4hc", ["xspp", INPUT_FILE, "-m", lz4hc_meta, "-o", lz4hc, "-a", "lz4", "--hc"]),
            base.Command("xspp zst", ["xspp", INPUT_FILE, "-m", zst_meta, "-o", zst, "-a", "zstd"])
        ],
        cleanup_commands=[base.Command("rm", ["rm", meta, lz4, lz4_meta, lz4hc, lz4hc_meta, zst, zst_meta])]
    )


def parse_args():
    parser = argparse.ArgumentParser(prog="xs_test", description="Automated test of xs grep")
    parser.add_argument("--list-benchmarks", action="store_true", help="List available benchmarks by name and exit")
    parser.add_argument("--exit-on-failure", action="store_true", help="Stop testing if a single test fails")
    parser.add_argument("--filter", metavar="FILTER", default="", help="Filter benchmarks by name using regex")
    parser.add_argument("--silent", action="store_true", help="Do not output log messages")

    return parser.parse_args()


if __name__ == "__main__":
    benchmarks = {
        "xsgrep literal ASCII": test_literal_ascii,
        "xsgrep regex ASCII": test_regex_ascii,
        "xsgrep literal ASCII (-b)": test_literal_ascii_byte_offsets,
        "xsgrep regex ASCII (-b)": test_regex_ascii_byte_offsets,
        "xsgrep literal ASCII (-n)": test_literal_ascii_line_numbers,
        "xsgrep regex ASCII (-n)": test_regex_ascii_line_numbers,
        "xsgrep literal ASCII (-f)": test_literal_ascii_fixed_string,
        "xsgrep literal ASCII (-i)": test_literal_ascii_ignore_case,
        "xsgrep regex ASCII (-i)": test_regex_ascii_ignore_case,
        "xsgrep literal ASCII (-o)": test_literal_ascii_match_only,
        "xsgrep regex ASCII (-o)": test_regex_ascii_match_only,
        "xsgrep preprocessed literal": test_preprocessed_literal,
        "xsgrep preprocessed regex": test_preprocessed_regex,
    }
    args = parse_args()
    EXIT_ON_FAIL = args.exit_on_failure
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
