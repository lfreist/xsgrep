[![Docker](https://github.com/lfreist/xsgrep/actions/workflows/docker-image.yml/badge.svg)](https://github.com/lfreist/xsgrep/actions/workflows/docker-image.yml)

[![Linux (clang)](https://github.com/lfreist/xsgrep/actions/workflows/build-linux-clang.yml/badge.svg)](https://github.com/lfreist/xsgrep/actions/workflows/build-linux-clang.yml)
[![Linux (gcc)](https://github.com/lfreist/xsgrep/actions/workflows/build-linux-gcc.yml/badge.svg)](https://github.com/lfreist/xsgrep/actions/workflows/build-linux-gcc.yml)

[![Thread Sanitizer](https://github.com/lfreist/xsgrep/actions/workflows/thread-sanitizer-test.yml/badge.svg)](https://github.com/lfreist/xsgrep/actions/workflows/thread-sanitizer-test.yml)
[![Address Sanitizer](https://github.com/lfreist/xsgrep/actions/workflows/address-sanitizer-test.yml/badge.svg)](https://github.com/lfreist/xsgrep/actions/workflows/address-sanitizer-test.yml)

[![Test Executables](https://github.com/lfreist/xsgrep/actions/workflows/exe-test.yml/badge.svg)](https://github.com/lfreist/xsgrep/actions/workflows/exe-test.yml)

[![Code Style (clang14)](https://github.com/lfreist/xsgrep/actions/workflows/clang-format.yml/badge.svg)](https://github.com/lfreist/xsgrep/actions/workflows/clang-format.yml)


# xsgrep
A grep like command line text search tool implemented using x-search library

## Build
```
git clone https://github.com/lfreist/xsgrep
cd xsgrep
make build
```

## Test
```
make test
```

## Benchmark
> **Important:**
>
> Check `drop_cache.c`s content before running the listed commands. `drop_cache` should only do the following:
> - create a valid file descriptor to "/proc/sys/vm/drop_caches" in write mode
> - write a single byte ('3') to the file descriptor
> Done. Nothing more, nothing less!

Please run the following commands before running benchmarks:
```
gcc drop_cache.c -o drop_cache
sudo chown root:root drop_cache
sudo chmod +s drop_cache
ln -s drop_cache $HOME/drop_cache
```
> **Explanation:**
> 
> Running benchmarks requires permissions to drop the RAMs cache. However, (for good reasons) it requires root
> privileges to do so. We DO NOT want to run the full benchmark as root. Therefore, we compile a little program
> (`drop_cache.c`) that performs the RAM cache drop. This program (and nothing else) must run as root.
> Therefore, we set the mod of the file to always be executes as root.

Now, run the benchmarks: `make benchmark`