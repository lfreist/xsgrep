// Copyright 2023, Leon Freist
// Author: Leon Freist <freist@informatik.uni-freiburg.de>

#include "./GrepSearcher.h"

#include <xsearch/utils/InlineBench.h>

// ----- Helper function -------------------------------------------------------
// _____________________________________________________________________________
std::string get_regex_match_(const char* data, size_t size,
                             const re2::RE2& pattern) {
  re2::StringPiece input(data, size);
  re2::StringPiece match;
  re2::RE2::PartialMatch(input, pattern, &match);
  return match.as_string();
}

// ===== GrepSearcher ==========================================================
// _____________________________________________________________________________
GrepSearcher::GrepSearcher(std::string pattern, bool byte_offset,
                           bool line_number, bool only_matching, bool regex,
                           bool ignore_case, Grep::Locale locale)
    : _pattern(std::move(pattern)),
      _line_number(line_number),
      _byte_offset(byte_offset),
      _only_matching(only_matching),
      _regex(regex),
      _ignore_case(ignore_case),
      _locale(locale) {
  if (regex) {
    re2::RE2::Options re2_options;
    re2_options.set_posix_syntax(true);
    re2_options.set_case_sensitive(!_ignore_case);
    _re_pattern = std::make_unique<re2::RE2>('(' + _pattern + ')', re2_options);
  } else if (_ignore_case && _locale != Grep::Locale::ASCII) {
    // not regex, but ignore case and not ascii: use re2 and implicitly assume
    // pattern to be UTF-8
    re2::RE2::Options re2_options;
    re2_options.set_case_sensitive(false);
    auto escaped_pattern = xs::utils::str::escaped(_pattern);
    _re_pattern =
        std::make_unique<re2::RE2>('(' + escaped_pattern + ')', re2_options);
  }
}

// _____________________________________________________________________________
std::vector<Grep::Match> GrepSearcher::process(xs::DataChunk* data) const {
  INLINE_BENCHMARK_WALL_START(_, "search");
  if (_regex || (_ignore_case && _locale != Grep::Locale::ASCII)) {
    return process_regex(data);
  }
  return process_plain(data);
}

// _____________________________________________________________________________
std::vector<Grep::Match> GrepSearcher::process_regex(
    xs::DataChunk* data) const {
  std::vector<uint64_t> byte_offsets =
      _only_matching
          ? xs::search::regex::global_byte_offsets_match(data, *_re_pattern,
                                                         false)
          : xs::search::regex::global_byte_offsets_line(data, *_re_pattern);
  std::vector<uint64_t> line_numbers;
  if (_line_number) {
    line_numbers = xs::map::bytes::to_line_indices(data, byte_offsets);
    std::transform(line_numbers.begin(), line_numbers.end(),
                   line_numbers.begin(), [](uint64_t li) { return li + 1; });
  }
  std::vector<std::string> lines;
  if (_only_matching) {
    lines.resize(byte_offsets.size());
    std::transform(byte_offsets.begin(), byte_offsets.end(), lines.begin(),
                   [&](uint64_t index) {
                     size_t local_byte_offset =
                         index - data->getMetaData().original_offset;
                     return get_regex_match_(data->data() + local_byte_offset,
                                             data->size() - local_byte_offset,
                                             *_re_pattern);
                   });
  } else {
    lines.resize(byte_offsets.size());
    std::transform(
        byte_offsets.begin(), byte_offsets.end(), lines.begin(),
        [data](uint64_t index) { return xs::map::byte::to_line(data, index); });
  }

  std::vector<Grep::Match> res(byte_offsets.size());
  for (uint64_t i = 0; i < byte_offsets.size(); ++i) {
    res[i].line_number =
        _line_number ? static_cast<int64_t>(line_numbers[i]) : -1;
    res[i].byte_position = static_cast<int64_t>(byte_offsets[i]);
    res[i].match = lines[i];
  }
  return res;
}

// _____________________________________________________________________________
std::vector<Grep::Match> GrepSearcher::process_plain(
    xs::DataChunk* data) const {
  xs::DataChunk tmp_chunk;
  xs::DataChunk* op_chunk = data;
  std::string pattern = _pattern;
  if (_ignore_case && data->getMetaData().line_mapping_data.empty()) {
    tmp_chunk = xs::DataChunk(*data);
    // std::transform(data->data(), data->data() + data->size(),
    // tmp_chunk.data(), ::tolower);
    xs::utils::str::simd::toLower(tmp_chunk.data(), tmp_chunk.size());
    op_chunk = &tmp_chunk;
    std::transform(_pattern.begin(), _pattern.end(), pattern.begin(),
                   ::tolower);
  }
  std::vector<uint64_t> byte_offsets_match =
      xs::search::global_byte_offsets_match(op_chunk, pattern, !_only_matching);
  std::vector<uint64_t> byte_offsets_line;
  std::vector<uint64_t> line_numbers;
  if (_line_number) {
    line_numbers =
        xs::map::bytes::to_line_indices(op_chunk, byte_offsets_match);
    std::transform(line_numbers.begin(), line_numbers.end(),
                   line_numbers.begin(), [](uint64_t li) { return li + 1; });
  }
  std::vector<std::string> lines;
  lines.reserve(byte_offsets_match.size());
  if (_only_matching) {
    for (auto bo : byte_offsets_match) {
      lines.emplace_back(data->data() + bo - data->getMetaData().actual_offset,
                         _pattern.size());
    }
  } else {
    byte_offsets_line.resize(byte_offsets_match.size());
    std::transform(
        byte_offsets_match.begin(), byte_offsets_match.end(),
        byte_offsets_line.begin(), [data](uint64_t index) {
          return index - xs::search::previous_new_line_offset_relative_to_match(
                             data, index - data->getMetaData().actual_offset);
        });
    lines.resize(byte_offsets_match.size());
    std::transform(
        byte_offsets_line.begin(), byte_offsets_line.end(), lines.begin(),
        [data](uint64_t index) { return xs::map::byte::to_line(data, index); });
  }

  std::vector<Grep::Match> res(byte_offsets_match.size());
  for (uint64_t i = 0; i < byte_offsets_match.size(); ++i) {
    res[i].line_number =
        _line_number ? static_cast<int64_t>(line_numbers[i]) : -1;
    // TODO: include for only_matching stuff
    res[i].byte_position =
        _byte_offset ? static_cast<int64_t>(byte_offsets_line[i]) : -1;
    res[i].match = lines[i];
  }
  return res;
}