// Copyright 2023, Leon Freist
// Author: Leon Freist <freist@informatik.uni-freiburg.de>

#include "grep.h"

#include <xsearch/utils/string_utils.h>

#include "tasks/GrepOutput.h"
#include "tasks/GrepSearcher.h"

Grep::Grep(std::string pattern, std::string file) {
  _options.pattern = std::move(pattern);
  _options.file = std::move(file);
}

Grep::Grep(std::string pattern, std::string file, Grep::Options options)
    : _options(std::move(options)) {
  _options.pattern = std::move(pattern);
  _options.file = std::move(file);
  // these three members need to be set using setter method in case they are set
  //  to default values
  set_colored_output(_options.color);
  set_num_threads(_options.num_threads);
  set_locale(_options.locale);
}

Grep::Grep(Options options) : _options(std::move(options)) {
  // these three members need to be set using setter method in case they are set
  //  to default values
  set_colored_output(_options.color);
  set_num_threads(_options.num_threads);
  set_locale(_options.locale);
}

uint64_t Grep::count() {
  auto searcher = std::make_unique<xs::task::searcher::LineCounter>(
      _options.pattern, use_regex(), _options.ignore_case,
      _options.locale == Grep::Locale::UTF_8);
  auto executor =
      xs::Executor<xs::DataChunk, xs::result::base::CountResult, uint64_t>(
          _options.num_threads, get_reader(), get_processors(),
          std::move(searcher));
  executor.join();
  return executor.getResult()->size();
}

std::vector<Grep::Match> Grep::search() {
  auto searcher = std::make_unique<GrepSearcher>(
      _options.pattern, _options.byte_offset, _options.line_number,
      _options.only_matching, use_regex(), _options.ignore_case,
      _options.locale);
  auto executor = xs::Executor<xs::DataChunk, GrepOutput,
                               std::vector<Grep::Match>, Grep::Options>(
      _options.num_threads, get_reader(), get_processors(), std::move(searcher),
      std::move(_options));
  executor.join();
  return {};
}

void Grep::write(std::ostream* stream) {
  if (_options.count) {
    *stream << count() << '\n';
  } else {
    auto searcher = std::make_unique<GrepSearcher>(
        _options.pattern, _options.byte_offset, _options.line_number,
        _options.only_matching, use_regex(), _options.ignore_case,
        _options.locale);
    auto executor =
        xs::Executor<xs::DataChunk, GrepOutput, std::vector<Grep::Match>,
                     Grep::Options, std::ostream&>(
            _options.num_threads, get_reader(), get_processors(),
            std::move(searcher), std::move(_options), *stream);
    executor.join();
  }
}

Grep& Grep::set_file(std::string file) {
  _options.file = std::move(file);
  return *this;
}

Grep& Grep::set_pattern(std::string pattern) {
  _options.pattern = std::move(pattern);
  return *this;
}

Grep& Grep::set_count_only(bool val) {
  _options.count = val;
  if (_options.count) {
    _options.line_number = false;
    _options.byte_offset = false;
  }
  return *this;
}

Grep& Grep::set_fixed_string(bool val) {
  _options.fixed_string = val;
  return *this;
}

Grep& Grep::set_line_number(bool val) {
  _options.line_number = val;
  return *this;
}

Grep& Grep::set_byte_offset(bool val) {
  _options.byte_offset = val;
  return *this;
}

Grep& Grep::set_colored_output(Grep::Color color) {
  if (color == Grep::Color::AUTO) {
    if (isatty(STDOUT_FILENO)) {
      _options.color = Grep::Color::ON;
    } else {
      _options.color = Grep::Color::OFF;
    }
  } else {
    _options.color = color;
  }
  return *this;
}

Grep& Grep::set_only_matching(bool val) {
  _options.only_matching = val;
  return *this;
}

Grep& Grep::set_ignore_case(bool val) {
  _options.ignore_case = val;
  return *this;
}

Grep& Grep::set_locale(Locale locale) {
  if (locale == Grep::Locale::AUTO) {
    _options.locale = xs::utils::str::is_ascii(_options.pattern)
                          ? Grep::Locale::ASCII
                          : Grep::Locale::UTF_8;
  } else {
    _options.locale = locale;
  }
  return *this;
}

Grep& Grep::set_print_file_path(bool val) {
  _options.print_file_path = val;
  return *this;
}

Grep& Grep::set_use_mmap(bool val) {
  _options.no_mmap = val;
  return *this;
}

Grep& Grep::set_num_threads(int val) {
  int fallback_value = _max_phys_cores / 4;
  if (fallback_value < 2) {
    fallback_value = 2;
  }
  _options.num_threads = val < 1
                             ? fallback_value
                             : (val > _max_phys_cores ? _max_phys_cores : val);
  return *this;
}

const std::string& Grep::file() const { return _options.file; }

const std::string& Grep::pattern() const { return _options.pattern; }

bool Grep::count_only() const { return _options.count; }

bool Grep::fixed_string() const { return _options.fixed_string; }

bool Grep::line_number() const { return _options.line_number; }

bool Grep::byte_offset() const { return _options.byte_offset; }

Grep::Color Grep::colored_output() const { return _options.color; }

bool Grep::only_matching() const { return _options.only_matching; }

bool Grep::ignore_case() const { return _options.ignore_case; }

Grep::Locale Grep::locale() const { return _options.locale; }

bool Grep::print_file_path() const { return _options.print_file_path; }

bool Grep::use_mmap() const { return _options.no_mmap; }

int Grep::num_threads() const { return _options.num_threads; }

// ----- private ---------------------------------------------------------------
std::vector<Grep::base_processors> Grep::get_processors() const {
  std::vector<std::unique_ptr<xs::task::base::InplaceProcessor<xs::DataChunk>>>
      ret;
  if (_options.line_number) {
    ret.push_back(std::make_unique<xs::task::processor::NewLineSearcher>());
  }
  return ret;
}

Grep::base_reader Grep::get_reader() const {
  if (_options.no_mmap) {
    return std::make_unique<xs::task::reader::FileBlockReader>(_options.file);
  }
  return std::make_unique<xs::task::reader::FileBlockReaderMMAP>(_options.file);
}

bool Grep::use_regex() const {
  return xs::utils::use_str_as_regex(_options.pattern) &&
         !_options.fixed_string;
}

const int Grep::_max_phys_cores =
    static_cast<int>(std::thread::hardware_concurrency()) / 2;