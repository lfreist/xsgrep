NAME=xsgrep

.PHONY: all test check_style benchmark clean help install install_benchmark uninstall

help:
	@echo "--------------------------------------------------------------------------------"
	@echo "                                    xsgrep"
	@echo "A GNU grep like Executable built with x-search"
	@echo "Bachelor Project, 2023"
	@echo "Author    : Leon Freist <freist@informatik.uni-freiburg.de>"
	@echo "URL       : https://github.com/lfreist/xsgrep"
	@echo "Examiner  : Prof. Dr. Hannah Bast"
	@echo "Supervisor: Johannes Kalmbach"
	@echo "--------------------------------------------------------------------------------"
	@echo "The following commands (and more) are available:"
	@echo " - 'make build'"
	@echo " - 'make benchmark'"
	@echo " - 'make test'"
	@echo "--------------------------------------------------------------------------------"

all: check_style test benchmark clean

init:
	git submodule update --init --recursive 2>/dev/null

build: init
	cmake -B build -DCMAKE_BUILD_TYPE=Release -DRE2_BUILD_TESTING=off 2>/dev/null
	cmake --build build --config Release -j $(nproc) 2>/dev/null

build_benchmark: init
	cmake -B build-benchmark -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS="-DBENCHMARK" -DRE2_BUILD_TESTING=off -DXS_BENCHMARKS=ON 2>/dev/null
	cmake --build build-benchmark --config Benchmark -j $(nproc) 2>/dev/null

build_sanitizer: init
	cmake -B build-thread-sanitizer -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_CXX_FLAGS="-fsanitize=thread" -DCMAKE_CXX_COMPILER=/usr/bin/clang++-15 -DRE2_BUILD_TESTING=off
	cmake --build build-thread-sanitizer -j $(nproc) 2>/dev/null
	cmake -B build-address-sanitizer -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_CXX_FLAGS="-fsanitize=address" -DCMAKE_CXX_COMPILER=/usr/bin/clang++-15 -DRE2_BUILD_TESTING=off
	cmake --build build-address-sanitizer -j $(nproc) 2>/dev/null

test:
	python3 testsuit/cmdtest/test_xsgrep.py;

check_style:
	bash ./format_check.sh

benchmark: install_benchmark install
	python3 benchsuit/cmdbench/main.py --config benchsuit/suits --iterations 3 --output benchsuit/results/cache/$$(hostname) --cwd sample_data/ --sleep 10
	python3 benchsuit/cmdbench/main.py --config benchsuit/suits --iterations 3 --output benchsuit/results/no-cache/$$(hostname) --drop-cache "$$HOME/drop_cache" --cwd sample_data/ --sleep 10

install_benchmark: build_benchmark
	cp build-benchmark/src/xsgrep/xs $$HOME/.local/bin/benched_xs
	cp build-benchmark/src/benchutil/just_read $$HOME/.local/bin/just_read

install: build
	bash scripts/install.sh

uninstall:
	bash scripts/uninstall.sh

clean:
	rm -rf build
	rm -rf build-benchmark
	rm -rf build-address-sanitizer
	rm -rf build-thread-sanitizer