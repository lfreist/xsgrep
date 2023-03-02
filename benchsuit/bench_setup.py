import os.path
import subprocess
import requests
import argparse


def log(*args, **kwargs):
    print(80 * " ", end='\r', flush=True)
    print(*args, **kwargs)


def download(url: str, dest: str) -> None:
    """
    Download url to dest
    """
    with open(dest, "wb") as f:
        data = requests.get(url, stream=True)
        num_bytes_read = 0
        name = dest.split('/')[-1]
        for chunk in data.iter_content(chunk_size=32768):
            log(f"{dest}: {num_bytes_read / 1000000:.2f} MiB written", end='\r', flush=True)
            f.write(chunk)
            num_bytes_read += len(chunk)
        print()


def decompress(file_path: str) -> None:
    """
    decompress file_path using gunzip
    """
    log(f"Decompressing {file_path}...", end='\r', flush=True)
    subprocess.Popen(["gunzip", file_path]).communicate()
    log("Decompression done.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="bench_setup", description="Download data for benchmarks")
    parser.add_argument("--dir", metavar="PATH", default=os.path.join(os.getcwd(), "sample_data"),
                        help="Destination directory for downloaded files")
    args = parser.parse_args()

    URLs = [
        "https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2016/mono/en.txt.gz",  # english, plain ASCII
        # "https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2016/mono/el.txt.gz",  # greek, pure UTF-8 multi char
        # "https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2016/mono/es.txt.gz",  # spanish, mixed
    ]

    if not os.path.exists(args.dir):
        os.makedirs(args.dir)
    for url in URLs:
        file = url.split('/')[-1]
        file_path = os.path.join(args.dir, file)
        txt_file = os.path.join(args.dir, '.'.join(file.split('.')[:-1]))
        if not os.path.exists(txt_file):
            if not os.path.exists(file_path):
                download(url, file_path)
            decompress(file_path)
