FROM ubuntu:22.04

LABEL maintainer="Leon Freist <freist@informatik.uni-freiburg.de>"

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update > /dev/null
RUN apt-get install -y apt-utils build-essential git make vim cmake libzstd-dev liblz4-dev lz4 zstd ripgrep grep python3 python3-pip python3-venv  > /dev/null
RUN apt install -y libboost1.74-dev libboost-program-options1.74-dev > /dev/null
RUN rm -rf /var/lib/apt/lists/*

COPY . xsgrep
WORKDIR "xsgrep"
RUN git submodule update --init --recursive
RUN make help

# docker build -t leon-freist-bachelproject .
# docker run -it -v $(pwd)/files:/inputfiles/input:ro --name leon-freist-bachelorproject leon-freist-bachelorproject