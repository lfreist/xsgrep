// Copyright 2023, Leon Freist
// Author: Leon Freist <freist@informatik.uni-freiburg.de>

#pragma once

#include <xsearch/xsearch.h>

class GrepSearcher;
class GrepOutput;

class Grep {
  typedef std::unique_ptr<xs::task::base::DataProvider<xs::DataChunk>>
      base_reader;
  typedef std::unique_ptr<xs::task::base::InplaceProcessor<xs::DataChunk>>
      base_processors;

 public:
  struct Match {
    int64_t byte_position{-1};
    int64_t line_number{-1};
    std::string match;
  };

  enum class Color { AUTO, ON, OFF };

  enum class Locale { AUTO, ASCII, UTF_8 };

  /**
   * Options: A struct holding information about what xsgrep searches and how
   * results will be printed.
   *
   * @param count: Only count number of matches?
   * @param fixed_string: use pattern as fixed string, even if pattern is a
   * regex?
   * @param line_number: add line numbers to result
   * @param byte_offset: add byte offsets to result. If match_only is true, the
   *  byte offsets is the match position, if match_only is false, the byte
   *  offset is the position of the line containing the match
   * @param color: use colored output, default is AUTO?
   * @param only_matching: only print matches and search for match offsets
   * @param ignore_case: run case insensitive search
   * @param locale: use the provided encoding
   * @param print_file_path: print the file path before the matching content
   *  (only if the results are written to an ostream)
   * @param pattern: the pattern that is searched
   * @param file: the file that is searched
   * @param use_mmap: reader uses memory mapping if possible
   */
  struct Options {
    bool count = false;
    bool fixed_string = false;
    bool line_number = false;
    bool byte_offset = false;
    Color color = Color::AUTO;
    bool only_matching = false;
    bool ignore_case = true;
    Locale locale = Locale::ASCII;
    bool print_file_path = false;
    std::string pattern;
    std::string file;
    std::string meta_file_path;
    bool no_mmap = true;
    int num_threads = 0;
    int num_reader_threads = 1;
  };

  // Constructors
  Grep() = default;
  Grep(std::string pattern, std::string file);
  Grep(std::string pattern, std::string file, Options options);
  explicit Grep(Options options);

  uint64_t count();
  std::vector<Grep::Match> search();
  void write(std::ostream* stream = &std::cout);

  Grep& set_file(std::string file);
  Grep& set_meta_file(std::string meta_file);
  Grep& set_pattern(std::string pattern);
  Grep& set_count_only(bool val);
  Grep& set_fixed_string(bool val);
  Grep& set_line_number(bool val);
  Grep& set_byte_offset(bool val);
  Grep& set_colored_output(Color color);
  Grep& set_only_matching(bool val);
  Grep& set_ignore_case(bool val);
  Grep& set_locale(Locale locale);
  Grep& set_print_file_path(bool val);
  Grep& set_use_mmap(bool val);
  Grep& set_num_threads(int val);
  Grep& set_num_reader_threads(int val);

  [[nodiscard]] const std::string& file() const;
  [[nodiscard]] const std::string& meta_file() const;
  [[nodiscard]] const std::string& pattern() const;
  [[nodiscard]] bool count_only() const;
  [[nodiscard]] bool fixed_string() const;
  [[nodiscard]] bool line_number() const;
  [[nodiscard]] bool byte_offset() const;
  [[nodiscard]] Color colored_output() const;
  [[nodiscard]] bool only_matching() const;
  [[nodiscard]] bool ignore_case() const;
  [[nodiscard]] Locale locale() const;
  [[nodiscard]] bool print_file_path() const;
  [[nodiscard]] bool use_mmap() const;
  [[nodiscard]] int num_threads() const;
  [[nodiscard]] int num_reader_threads() const;

 private:
  [[nodiscard]] std::vector<base_processors> get_processors() const;

  [[nodiscard]] base_reader get_reader();

  [[nodiscard]] bool use_regex() const;

  /// number of physical cores available assuming CPU is hyper threaded.
  static const int _max_phys_cores;

  Options _options{};
};