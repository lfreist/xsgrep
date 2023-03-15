// Copyright 2023, Leon Freist
// Author: Leon Freist <freist@informatik.uni-freiburg.de>

#include <fstream>
#include <iostream>
#include <vector>

#define BLOCK_SIZE 16777216  // 16 MiB

int main(int argc, char** argv) {
  if (argc > 2) {
    std::cerr << "Usage: ./just_read <file_path>\n";
    return 1;
  }
  std::string file =
      argc == 1 ? std::string("/dev/stdin") : std::string(argv[2]);
  std::ifstream f(file);
  if (!f) {
    std::cerr << "Could not read '" << argv[1] << "'.\n";
    return 2;
  }
  // read the file in 16 MiB blocks
  std::vector<char> buffer(BLOCK_SIZE);
  int s = 0;
  while (true) {
    f.read(buffer.data(), BLOCK_SIZE);
    if (f.eof()) {
      break;
    }
    // do one simple operation per chunk to avoid that the compiler optimizes
    // the full read away
    s += buffer.back();
  }
  std::cout << s << std::endl;
}