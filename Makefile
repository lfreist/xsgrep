NAME=xsgrep

.PHONY: all test check_style benchmark clean help install

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

setup_venv:
	python3 -m venv venv; . venv/bin/activate; python3 -m pip install -r requirements.txt

test: setup_venv
	. venv/bin/activate; python3 testsuit/test_xsgrep.py;

check_style:
	bash ./format_check.sh

benchmark: build_benchmark

install: build
	cp build/src/xs ~/.local/bin/xs
	cp build/src/xspp/xspp ~/.local/bin/xspp

clean:
	rm -rf build
	rm -rf build-benchmark
	rm -rf build-address-sanitizer
	rm -rf build-thread-sanitizer