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
            log(f"{num_bytes_read / 1000000:.2f} MiB written", end='\r', flush=True)
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

    URLs = {
        "en": "https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2016/mono/en.txt.gz",  # english, plain ASCII
        "el": "https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2016/mono/el.txt.gz",  # greek, pure UTF-8 multi char
        "es": "https://object.pouta.csc.fi/OPUS-OpenSubtitles/v2016/mono/es.txt.gz",  # spanish, mixed
    }

    for folder, url in URLs.items():
        if not os.path.exists(os.path.join(args.dir, folder)):
            os.makedirs(os.path.join(args.dir, folder))
        file_path = os.path.join(args.dir, folder, "data.txt.gz")
        txt_file = os.path.join(args.dir, folder, "data.txt")
        if not os.path.exists(txt_file):
            if not os.path.exists(file_path):
                print(f" downloading {url!r} to {file_path!r}...", end=" ")
                download(url, file_path)
                print("DONE")
            print(f" decompressing {file_path!r} to {txt_file!r}...", end=" ")
            decompress(file_path)
            print("DONE")
