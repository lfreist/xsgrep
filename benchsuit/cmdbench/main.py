import os.path

import base
import gnu_time_benchmark as gnutime
import InlineBench_benchmark as InlineBench

import argparse
import json


class UnknownTimerError(Exception):
    def __init__(self, timer: str):
        self.timer = timer

    def __str__(self):
        return f"{self.timer}. Choose from ['GNU time', 'InlineBench']"


def parse_config(path: str, cwd: str | None = None) -> base.Benchmark:
    with open(path, "r") as f:
        data = json.load(f)
    if data["timer"].lower() == "gnu time":
        commands = [
            gnutime.GNUTimeCommand(name=name, cmd=cmd, cwd=cwd) for name, cmd in data["commands"].items()
        ]
        return gnutime.GNUTimeBenchmark(
            data["name"],
            commands=commands,
            setup_commands=[base.Command(cmd[0], cmd=cmd, cwd=cwd) for cmd in data["setup_cmd"]],
            cleanup_commands=[base.Command(cmd[0], cmd=cmd, cwd=cwd) for cmd in data["cleanup_cmd"]],
            sleep=args.sleep
        )
    elif data["timer"].lower() == "inlinebench":
        commands = [
            InlineBench.InlineBenchCommand(name=name, cmd=cmd, cwd=cwd) for name, cmd in data["commands"].items()
        ]
        return InlineBench.InlineBenchBenchmark(
            data["name"],
            commands=commands,
            setup_commands=[base.Command(cmd[0], cmd=cmd, cwd=cwd) for cmd in data["setup_cmd"]],
            cleanup_commands=[base.Command(cmd[0], cmd=cmd, cwd=cwd) for cmd in data["cleanup_cmd"]],
            sleep=args.sleep
        )
    else:
        raise UnknownTimerError(data["timer"])


def read_result_info_data(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


def write_result_info_data(meta_data: dict, path: str):
    with open(path, "w") as f:
        json.dump(meta_data, f)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="cmdbench",
                                     description="Compare command line tools")
    parser.add_argument("--config", metavar="PATH", nargs='+', required=True,
                        help="Path to directory containing config file or path to config file")
    parser.add_argument("--cwd", metavar="PATH", default=os.path.join(os.getcwd()),
                        help="Directory containing files. If config files contain absolute or valid relative paths "
                             "this argument can be ignored.")
    parser.add_argument("--list-benchmarks", action="store_true", help="List available benchmarks by name and exit")
    parser.add_argument("--drop-cache", metavar="PATH", help="Path to executable that drops RAM caches", default="")
    parser.add_argument("--iterations", "-i", metavar="INTEGER", type=int, default=3,
                        help="Number of iterations per benchmark")
    parser.add_argument("--sleep", "-p", metavar="INTEGER", type=int, default=0,
                        help="sleep x seconds between running benchmarks")
    parser.add_argument("--output", "-o", metavar="PATH", default="",
                        help="The directory where results are written to")

    return parser.parse_args()


def main(conf_file: str, cwd: str | None, out_dir: str) -> None:
    bm = parse_config(conf_file, cwd=cwd)
    if bm is None:
        print("No valid config files found.")
        exit(2)
    bm.iterations = args.iterations
    bm.drop_cache = args.drop_cache
    if args.drop_cache != "":
        bm.drop_cache = base.Command("drop cache", cmd=[args.drop_cache])
    else:
        bm.drop_cache = None
    gnutime.log(f" Running {bm.name}:")
    result = bm.run()
    if out_dir:
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        result_info_data = read_result_info_data(result_meta_data)
        tmp_id = 0
        file_name = bm.name.replace(" ", "_")
        tmp_file_name = f"{file_name}_{tmp_id}.json"
        while os.path.exists(os.path.join(out_dir, tmp_file_name)):
            tmp_id += 1
            tmp_file_name = f"{file_name}_{tmp_id}.json"
        file_name = f"{file_name}_{tmp_id}"
        output_file = os.path.join(out_dir, file_name)
        result_info_data[file_name + ".json"] = result.get_setup()
        result_info_data[file_name + ".json"]["plot"] = file_name + ".pdf"
        result_info_data[file_name + ".json"]["config_file"] = conf_file
        write_result_info_data(result_info_data, result_meta_data)
        result.write_json(output_file + ".json")
        result.plot(output_file + ".pdf")
    else:
        result.plot()


def recursive_files(path: str):
    for obj in os.listdir(path):
        p = os.path.join(path, obj)
        if os.path.isdir(p):
            recursive_files(p)
        if os.path.isfile(p) and obj.endswith(".json"):
            main(p, args.cwd, args.output)


if __name__ == "__main__":
    import warnings
    warnings.filterwarnings("ignore")

    args = parse_arguments()
    result_meta_data = f"{args.output}.results.meta.json"

    for conf in args.config:
        if not os.path.exists(conf):
            print(f"ERROR: {conf} does not exist.")
            exit(1)
        bm = None
        if os.path.isdir(conf):
            recursive_files(conf)
        else:
            main(conf, args.cwd, args.output)

