import json
import os
import statistics
import sys
import math

import pandas as pd


def read_res_json(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def get_all_results(path: str):
    if os.path.isfile(path) and path.endswith(".json") and "meta" not in path:
        yield path, read_res_json(path)
    if os.path.isdir(path):
        for obj in os.listdir(path):
            yield from get_all_results(os.path.join(path, obj))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = os.getcwd()
    print(f"Reading data from base directory {path!r}")
    for file, data in get_all_results(path):
        print(f" -> {file}")
        d = {"time": ["Wall", "CPU"]}
        for run, value in data["results"].items():
            d[run] = [statistics.mean(value['data']['wall [s]']), statistics.mean(value['data']['cpu [s]'])]
        a = pd.DataFrame(d)
        with open(f"{file}.txt", "w") as f:
            print(a, file=f)
