#!/usr/bin/env bash

# text search (no regex)
# ascii xs
python3 benchsuit/xs_benchmarks.py cmake-build-benchmark/src/xs --iterations 5 -o benchsuit/results/xs/cache/ascii/literal/$(hostname) --input-file sample_data/en.sample.txt --pattern Sherlock
python3 benchsuit/xs_benchmarks.py cmake-build-benchmark/src/xs --iterations 5 --drop-cache -o benchsuit/results/xs/no-cache/ascii/literal/$(hostname) --input-file sample_data/en.sample.txt --pattern Sherlock

# utf8 xs
python3 benchsuit/xs_benchmarks.py cmake-build-benchmark/src/xs --iterations 5 -o benchsuit/results/xs/cache/utf8/literal/$(hostname) --input-file sample_data/el.sample.txt --pattern Σέρλοκ
python3 benchsuit/xs_benchmarks.py cmake-build-benchmark/src/xs --iterations 5 --drop-cache -o benchsuit/results/xs/no-cache/utf8/literal/$(hostname) --input-file sample_data/el.sample.txt --pattern Σέρλοκ

# text search (regex)
# ascii xs
python3 benchsuit/xs_benchmarks.py cmake-build-benchmark/src/xs --iterations 5 -o benchsuit/results/xs/cache/ascii/regex/$(hostname) --input-file sample_data/en.sample.txt --pattern "She[r ]lock"
python3 benchsuit/xs_benchmarks.py cmake-build-benchmark/src/xs --iterations 5 --drop-cache -o benchsuit/results/xs/no-cache/ascii/regex/$(hostname) --input-file sample_data/en.sample.txt --pattern "She[r ]lock"

# utf8 xs
python3 benchsuit/xs_benchmarks.py cmake-build-benchmark/src/xs --iterations 5 -o benchsuit/results/xs/cache/utf8/regex/$(hostname) --input-file sample_data/el.sample.txt --pattern "Σέρ[λοκ]"
python3 benchsuit/xs_benchmarks.py cmake-build-benchmark/src/xs --iterations 5 --drop-cache -o benchsuit/results/xs/no-cache/utf8/regex/$(hostname) --input-file sample_data/el.sample.txt --pattern "Σέρ[λοκ]"

# compares
# ascii
python3 benchsuit/search_tools_benchmarks.py --iterations 5 -o benchsuit/results/search_tools/cache/ascii/literal/$(hostname) --input-file sample_data/en.sample.txt --pattern Sherlock --filter literal
python3 benchsuit/search_tools_benchmarks.py --iterations 5 --drop-cache -o benchsuit/results/search_tools/no-cache/ascii/literal/$(hostname) --input-file sample_data/en.sample.txt --pattern Sherlock --filter literal

python3 benchsuit/search_tools_benchmarks.py --iterations 5 -o benchsuit/results/search_tools/cache/ascii/regex/$(hostname) --input-file sample_data/en.sample.txt --pattern "She[r ]lock" --filter regex
python3 benchsuit/search_tools_benchmarks.py --iterations 5 --drop-cache -o benchsuit/results/search_tools/no-cache/ascii/regex/$(hostname) --input-file sample_data/en.sample.txt --pattern "She[r ]lock" --filter regex

#utf8
python3 benchsuit/search_tools_benchmarks.py --iterations 5 -o benchsuit/results/search_tools/cache/utf8/literal/$(hostname) --input-file sample_data/el.sample.txt --pattern Σέρλοκ --filter literal
python3 benchsuit/search_tools_benchmarks.py --iterations 5 --drop-cache -o benchsuit/results/search_tools/no-cache/utf8/literal/$(hostname) --input-file sample_data/el.sample.txt --pattern Σέρλοκ --filter literal

python3 benchsuit/search_tools_benchmarks.py --iterations 5 -o benchsuit/results/search_tools/cache/utf8/regex/$(hostname) --input-file sample_data/el.sample.txt --pattern "Σέρ[λοκ]" --filter regex
python3 benchsuit/search_tools_benchmarks.py --iterations 5 --drop-cache -o benchsuit/results/search_tools/no-cache/utf8/regex/$(hostname) --input-file sample_data/el.sample.txt --pattern "Σέρ[λοκ]" --filter regex