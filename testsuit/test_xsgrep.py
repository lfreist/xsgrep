"""
Copyright 2023, Leon Freist
Author: Leon Freist <freist@informatik.uni-freiburg.de>

Test xsgrep by comparing its output to GNU grep
"""
import argparse
import os
import re
import subprocess

import requests
import cmdtest as ct

ASCII_FILE = "en.sample.txt"
UTF8_FILE = "el.sample.txt"

DATA_DIR = "sample_files"

DOWNLOADS = {
    "en.sample.txt": "https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2016/mono/en.txt.gz",
    "el.sample.txt": "https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2016/mono/el.txt.gz"
}

ASCII_PATTERN = "Sherlock"
UTF8_PATTERN = "Σέρλοκ"

ASCII_RE = "She[r ]lock"
UTF8_RE = "Σέρ[λοκ]"

EXIT_ON_FAIL = False


def test_plain_ascii() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", ASCII_PATTERN, os.path.join(DATA_DIR, ASCII_FILE)])
    commands = [
        ct.Command("xs", ["xs", ASCII_PATTERN, os.path.join(DATA_DIR, ASCII_FILE)]),
        ct.Command("xs -j 1", ["xs", ASCII_PATTERN, os.path.join(DATA_DIR, ASCII_FILE), "-j", "1"]),
    ]
    return ct.TestSuit(
        "ASCII search",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_utf8() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", UTF8_PATTERN, os.path.join(DATA_DIR, UTF8_FILE)])
    commands = [
        ct.Command("xs", ["xs", UTF8_PATTERN, os.path.join(DATA_DIR, UTF8_FILE)]),
        ct.Command("xs -j 1", ["xs", UTF8_PATTERN, os.path.join(DATA_DIR, UTF8_FILE), "-j", "1"]),
    ]
    return ct.TestSuit(
        "UTF-8 search",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_regex_ascii() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE)])
    commands = [
        ct.Command("xs", ["xs", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE)]),
        ct.Command("xs -j 1", ["xs", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-j", "1"]),
    ]
    return ct.TestSuit(
        "UTF-8 regex search",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_regex_utf8() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE)])
    commands = [
        ct.Command("xs", ["xs", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE)]),
        ct.Command("xs -j 1", ["xs", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-j", "1"]),
    ]
    return ct.TestSuit(
        "UTF-8 regex search",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_ascii_line_numbers() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", ASCII_PATTERN, os.path.join(DATA_DIR, ASCII_FILE), "-n"])
    commands = [
        ct.Command("xs", ["xs", ASCII_PATTERN, os.path.join(DATA_DIR, ASCII_FILE), "-n"]),
        ct.Command("xs -j 1", ["xs", ASCII_PATTERN, os.path.join(DATA_DIR, ASCII_FILE), "-j", "1", "-n"]),
    ]
    return ct.TestSuit(
        "ASCII search (-n)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_utf8_line_numbers() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", UTF8_PATTERN, os.path.join(DATA_DIR, UTF8_FILE), "-n"])
    commands = [
        ct.Command("xs", ["xs", UTF8_PATTERN, os.path.join(DATA_DIR, UTF8_FILE), "-n"]),
        ct.Command("xs -j 1", ["xs", UTF8_PATTERN, os.path.join(DATA_DIR, UTF8_FILE), "-j", "1", "-n"]),
    ]
    return ct.TestSuit(
        "UTF-8 search (-n)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_regex_ascii_line_numbers() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-n"])
    commands = [
        ct.Command("xs", ["xs", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-n"]),
        ct.Command("xs -j 1", ["xs", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-j", "1", "-n"]),
    ]
    return ct.TestSuit(
        "UTF-8 regex search (-n)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_regex_utf8_line_numbers() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-n"])
    commands = [
        ct.Command("xs", ["xs", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-n"]),
        ct.Command("xs -j 1", ["xs", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-j", "1", "-n"]),
    ]
    return ct.TestSuit(
        "UTF-8 regex search (-n)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_ascii_ignore_case() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", ASCII_PATTERN, os.path.join(DATA_DIR, ASCII_FILE), "-i"])
    commands = [
        ct.Command("xs", ["xs", ASCII_PATTERN, os.path.join(DATA_DIR, ASCII_FILE), "-i"]),
        ct.Command("xs -j 1", ["xs", ASCII_PATTERN, os.path.join(DATA_DIR, ASCII_FILE), "-j", "1", "-i"]),
    ]
    return ct.TestSuit(
        "ASCII search (-i)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_utf8_ignore_case() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", UTF8_PATTERN, os.path.join(DATA_DIR, UTF8_FILE), "-i"])
    commands = [
        ct.Command("xs", ["xs", UTF8_PATTERN, os.path.join(DATA_DIR, UTF8_FILE), "-i"]),
        ct.Command("xs -j 1", ["xs", UTF8_PATTERN, os.path.join(DATA_DIR, UTF8_FILE), "-j", "1", "-i"]),
    ]
    return ct.TestSuit(
        "UTF-8 search (-i)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_regex_ascii_ignore_case() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-i"])
    commands = [
        ct.Command("xs", ["xs", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-i"]),
        ct.Command("xs -j 1", ["xs", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-j", "1", "-i"]),
    ]
    return ct.TestSuit(
        "UTF-8 regex search (-i)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_regex_utf8_ignore_case() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-i"])
    commands = [
        ct.Command("xs", ["xs", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-i"]),
        ct.Command("xs -j 1", ["xs", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-j", "1", "-i"]),
    ]
    return ct.TestSuit(
        "UTF-8 regex search (-i)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_ascii_byte_offsets() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", ASCII_PATTERN, os.path.join(DATA_DIR, ASCII_FILE), "-b"])
    commands = [
        ct.Command("xs", ["xs", ASCII_PATTERN, os.path.join(DATA_DIR, ASCII_FILE), "-b"]),
        ct.Command("xs -j 1", ["xs", ASCII_PATTERN, os.path.join(DATA_DIR, ASCII_FILE), "-j", "1", "-b"]),
    ]
    return ct.TestSuit(
        "ASCII search (-b)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_utf8_byte_offsets() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", UTF8_PATTERN, os.path.join(DATA_DIR, UTF8_FILE), "-b"])
    commands = [
        ct.Command("xs", ["xs", UTF8_PATTERN, os.path.join(DATA_DIR, UTF8_FILE), "-b"]),
        ct.Command("xs -j 1", ["xs", UTF8_PATTERN, os.path.join(DATA_DIR, UTF8_FILE), "-j", "1", "-b"]),
    ]
    return ct.TestSuit(
        "UTF-8 search (-b)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_regex_ascii_byte_offsets() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-b"])
    commands = [
        ct.Command("xs", ["xs", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-b"]),
        ct.Command("xs -j 1", ["xs", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-j", "1", "-b"]),
    ]
    return ct.TestSuit(
        "UTF-8 regex search (-b)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_regex_utf8_byte_offsets() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-b"])
    commands = [
        ct.Command("xs", ["xs", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-b"]),
        ct.Command("xs -j 1", ["xs", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-j", "1", "-b"]),
    ]
    return ct.TestSuit(
        "UTF-8 regex search (-b)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_ascii_match_only() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", ASCII_PATTERN, os.path.join(DATA_DIR, ASCII_FILE), "-o"])
    commands = [
        ct.Command("xs", ["xs", ASCII_PATTERN, os.path.join(DATA_DIR, ASCII_FILE), "-o"]),
        ct.Command("xs -j 1", ["xs", ASCII_PATTERN, os.path.join(DATA_DIR, ASCII_FILE), "-j", "1", "-o"]),
    ]
    return ct.TestSuit(
        "ASCII search (-o)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_utf8_match_only() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", UTF8_PATTERN, os.path.join(DATA_DIR, UTF8_FILE), "-o"])
    commands = [
        ct.Command("xs", ["xs", UTF8_PATTERN, os.path.join(DATA_DIR, UTF8_FILE), "-o"]),
        ct.Command("xs -j 1", ["xs", UTF8_PATTERN, os.path.join(DATA_DIR, UTF8_FILE), "-j", "1", "-o"]),
    ]
    return ct.TestSuit(
        "UTF-8 search (-o)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_regex_ascii_match_only() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-o"])
    commands = [
        ct.Command("xs", ["xs", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-o"]),
        ct.Command("xs -j 1", ["xs", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-j", "1", "-o"]),
    ]
    return ct.TestSuit(
        "UTF-8 regex search (-o)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_regex_utf8_match_only() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-o"])
    commands = [
        ct.Command("xs", ["xs", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-o"]),
        ct.Command("xs -j 1", ["xs", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-j", "1", "-o"]),
    ]
    return ct.TestSuit(
        "UTF-8 regex search (-o)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_ascii_fixed_string() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-F"])
    commands = [
        ct.Command("xs", ["xs", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-F"]),
        ct.Command("xs -j 1", ["xs", ASCII_RE, os.path.join(DATA_DIR, ASCII_FILE), "-j", "1", "-F"]),
    ]
    return ct.TestSuit(
        "ASCII search (-F)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def test_plain_utf8_fixed_string() -> ct.TestSuit:
    ref_command = ct.ReferenceCommand("grep", ["grep", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-F"])
    commands = [
        ct.Command("xs", ["xs", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-F"]),
        ct.Command("xs -j 1", ["xs", UTF8_RE, os.path.join(DATA_DIR, UTF8_FILE), "-j", "1", "-F"]),
    ]
    return ct.TestSuit(
        "UTF-8 search (-F)",
        commands=commands,
        reference_command=ref_command,
        exit_on_fail=EXIT_ON_FAIL
    )


def download():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    for name, url in DOWNLOADS.items():
        if not os.path.exists(os.path.join(DATA_DIR, name)):
            ct.log(f"⏳ Downloading data {name!r}")
            data = requests.get(url, stream=True)
            num_bytes = 0
            with open(os.path.join(DATA_DIR, name) + ".gz", "wb") as f:
                for chunk in data.iter_content(chunk_size=16384):
                    ct.log(f"{num_bytes / 1000000:.2f} MiB written", end='\r', flush=True)
                    f.write(chunk)
                    num_bytes += len(chunk)
            ct.log("✅ download done")


def decompress():
    for name, _ in DOWNLOADS.items():
        path = os.path.join(DATA_DIR, name)
        if os.path.exists(path + ".gz"):
            ct.log(f"⏳ decompressing data {name!r}")
            p = subprocess.Popen(["gunzip", path + ".gz"])
            p.wait()
            ct.log("✅ decompression done")


def parse_args():
    parser = argparse.ArgumentParser(prog="xs_test",
                                     description="Automated test of xs grep")
    parser.add_argument("--dir", metavar="PATH", default=os.path.join(os.getcwd(), "sample_data"),
                        help="The directory data are downloaded to")
    parser.add_argument("--list-benchmarks", action="store_true", help="List available benchmarks by name and exit")
    parser.add_argument("--exit-on-failure", action="store_true", help="Stop testing if a single test fails")
    parser.add_argument("--filter", metavar="FILTER", default="", help="Filter benchmarks by name using regex")
    parser.add_argument("--silent", action="store_true", help="Do not output log messages")

    return parser.parse_args()


if __name__ == "__main__":
    benchmarks = {
        "xsgrep plain ASCII": test_plain_ascii,
        "xsgrep plain UTF-8": test_plain_utf8,
        "xsgrep regex ASCII": test_regex_ascii,
        "xsgrep regex UTF-8": test_regex_utf8,
        "xsgrep plain ASCII (-b)": test_plain_ascii_byte_offsets,
        "xsgrep plain UTF-8 (-b)": test_plain_utf8_byte_offsets,
        "xsgrep regex ASCII (-b)": test_regex_ascii_byte_offsets,
        "xsgrep regex UTF-8 (-b)": test_regex_utf8_byte_offsets,
        "xsgrep plain ASCII (-n)": test_plain_ascii_line_numbers,
        "xsgrep plain UTF-8 (-n)": test_plain_utf8_line_numbers,
        "xsgrep regex ASCII (-n)": test_regex_ascii_line_numbers,
        "xsgrep regex UTF-8 (-n)": test_regex_utf8_line_numbers,
        "xsgrep plain ASCII (-f)": test_plain_ascii_fixed_string,
        "xsgrep plain UTF-8 (-f)": test_plain_utf8_fixed_string,
        "xsgrep plain ASCII (-i)": test_plain_ascii_ignore_case,
        "xsgrep plain UTF-8 (-i)": test_plain_utf8_ignore_case,
        "xsgrep regex ASCII (-i)": test_regex_ascii_ignore_case,
        "xsgrep regex UTF-8 (-i)": test_regex_utf8_ignore_case,
        "xsgrep plain ASCII (-o)": test_plain_ascii_match_only,
        "xsgrep plain UTF-8 (-o)": test_plain_utf8_match_only,
        "xsgrep regex ASCII (-o)": test_regex_ascii_match_only,
        "xsgrep regex UTF-8 (-o)": test_regex_utf8_match_only,
    }
    args = parse_args()
    EXIT_ON_FAIL = args.exit_on_failure
    ct.SILENT = args.silent
    if args.list_benchmarks:
        print("The following benchmarks are available:")
        for name in benchmarks.keys():
            print(f" - {name}")
        exit(0)
    if args.dir:
        if os.path.exists(args.dir) and os.path.isdir(args.dir):
            DATA_DIR = args.dir
        else:
            print(f"{args.dir!r} is not a directory or does not exist")
            exit(1)

    download()
    decompress()

    for name, bm_func in benchmarks.items():
        res = None
        if re.search(args.filter, name):
            res = bm_func().run()
        print(res)
