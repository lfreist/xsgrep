import json
import os
import statistics
import sys
import math


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
        prev_C = -1
        prev_T = -1
        for run, value in data["results"].items():
            C = statistics.mean(value['data']['cpu [s]'])
            T = statistics.mean(value['data']['wall [s]'])
            print(f"    {run}")
            print(f"       wall: {T}")
            print(f"       cpu: {C}")
            if prev_T >= 0 and prev_C >= 0:
                dC = C - prev_C
                dT = prev_T - T
                if dT == 0:
                    dT = 0.000000000001
                print(f"       dC/dT: {dC / dT}")
            prev_C = C
            prev_T = T
        print()
