// Copyright 2023, Leon Freist
// Author: Leon Freist <freist@informatik.uni-freiburg.de>

#include <xsearch/xsearch.h>
#include <xsgrep/grep.h>

#include <boost/program_options.hpp>
#include <iostream>

namespace po = boost::program_options;

void print_version() {
  std::cout << "xs (xs grep) 1.0\n";
  std::cout << "Copyright (C) 2023 Leon Freist\n";
  std::cout << "Written in the scope of the Undergraduate Thesis of Leon "
               "Freist at the chair of Algorithms and Datastructures "
               "(University of Freiburg).\n";
  std::cout << "Examiner:   Prof. Dr. Hannah Bast\n";
  std::cout << "Supervisor: Johannes Kalmbach\n";
  std::cout << '\n';
  std::cout << "Written by Leon Freist; see\n";
  std::cout << "<https://github.com/lfreist/xsgrep>\n";
}

int main(int argc, char** argv) {
  INLINE_BENCHMARK_WALL_START(_, "total");
#ifdef BENCHMARK
  std::string benchmark_file;
  std::string benchmark_format;
#endif
  Grep::Options grep_options;

  po::options_description options("Options for xsgrep");
  po::positional_options_description positional_options;

  // wrappers for adding command line arguments
  // --------------------------------
  auto add_positional =
      [&positional_options]<typename... Args>(Args&&... args) {
        positional_options.add(std::forward<Args>(args)...);
      };
  auto add = [&options]<typename... Args>(Args&&... args) {
    options.add_options()(std::forward<Args>(args)...);
  };

  // defining possible command line arguments
  // ----------------------------------
  add_positional("PATTERN", 1);
  add_positional("PATH", 1);
  add("PATTERN", po::value<std::string>(&grep_options.pattern)->required(),
      "search pattern");
  add("PATH", po::value<std::string>(&grep_options.file)->default_value(""),
      "input file, stdin if '-' or empty");
  add("metafile,m",
      po::value<std::string>(&grep_options.meta_file_path)->default_value(""),
      "metafile of the corresponding FILE");
  add("help,h", "prints this help message");
  add("version,V", "display version information and exit");
  add("threads,j",
      po::value<int>(&grep_options.num_threads)
          ->default_value(0)
          ->implicit_value(-1),
      "number of threads");
  add("max-readers",
      po::value<int>(&grep_options.num_reader_threads)->default_value(1),
      "number of concurrently reading tasks (default is number of threads");
  add("count,c", po::bool_switch(&grep_options.count),
      "print only a count of selected lines");
  add("byte-offset,b", po::bool_switch(&grep_options.byte_offset),
      "print the byte offset with output lines");
  add("line-number,n", po::bool_switch(&grep_options.line_number),
      "print line number with output lines");
  add("only-matching,o", po::bool_switch(&grep_options.only_matching),
      "show only nonempty parts of lines that match");
  add("ignore-case,i",
      po::bool_switch(&grep_options.ignore_case)->default_value(false),
      "ignore case distinctions in patterns and data");
  add("fixed-strings,F",
      po::bool_switch(&grep_options.fixed_string)->default_value(false),
      "PATTERN is string (force no regex)");
  add("no-mmap", po::bool_switch(&grep_options.no_mmap)->default_value(false),
      "do not use mmap but read data instead");
#ifdef BENCHMARK
  add("benchmark-file", po::value<std::string>(&benchmark_file),
      "set output file of benchmark measurements.");
  add("benchmark-format",
      po::value<std::string>(&benchmark_format)->default_value("json"),
      "specify the output format of benchmark measurements (plain, json, "
      "csv");
#endif

  // parse command line options
  // ------------------------------------------------
  po::variables_map optionsMap;
  try {
    po::store(po::command_line_parser(argc, argv)
                  .options(options)
                  .positional(positional_options)
                  .run(),
              optionsMap);
    if (optionsMap.count("help")) {
      std::cout << options << std::endl;
      return 0;
    }
    if (optionsMap.count("version")) {
      print_version();
      return 0;
    }
    po::notify(optionsMap);
  } catch (const std::exception& e) {
    std::cerr << "Error in command line argument: " << e.what() << std::endl;
    std::cerr << options << std::endl;
    return 1;
  }

  Grep grep(grep_options);
  grep.write();

  INLINE_BENCHMARK_WALL_STOP("total");
#ifdef BENCHMARK
  if (optionsMap.count("benchmark-file")) {
    std::ofstream out_stream(benchmark_file);
    out_stream << INLINE_BENCHMARK_REPORT(benchmark_format);
  } else {
    std::cerr << INLINE_BENCHMARK_REPORT(benchmark_format) << std::endl;
  }
#endif
  return 0;
}