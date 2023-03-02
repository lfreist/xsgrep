#!/usr/bin/env bash

python3 benchsuit/cmdbench/main.py --config benchsuit/suits/xsgrep/ --iterations 1 -o benchsuit/results/xs/cache/$(hostname)
python3 benchsuit/cmdbench/main.py --config benchsuit/suits/xsgrep/ --iterations 1 -o benchsuit/results/xs/no-cache/$(hostname) --drop-cache "$HOME/drop_ram_caches"

python3 benchsuit/cmdbench/main.py --config benchsuit/suits/search_tools --iterations 1 -o benchsuit/results/search_tools/cache/$(hostname)
python3 benchsuit/cmdbench/main.py --config benchsuit/suits/search_tools --iterations 1 -o benchsuit/results/search_tools/cache/$(hostname)  --drop-cache "$HOME/drop_ram_caches"