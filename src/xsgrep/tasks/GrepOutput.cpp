// Copyright 2023, Leon Freist
// Author: Leon Freist <freist@informatik.uni-freiburg.de>

#include "./GrepOutput.h"

#include <xsearch/utils/InlineBench.h>

// ===== GrepOutput ============================================================
// _____________________________________________________________________________
GrepOutput::GrepOutput(Grep::Options options, std::ostream& ostream)
    : _options(std::move(options)), _ostream(ostream) {}

// _____________________________________________________________________________
void GrepOutput::add(std::vector<Grep::Match> partial_result, uint64_t id) {
  std::unique_lock lock(*this->_mutex);
  if (_current_index == id) {
    add(std::move(partial_result));
    _current_index++;
    // check if buffered results can be added now
    while (true) {
      auto search = _buffer.find(_current_index);
      if (search == _buffer.end()) {
        break;
      }
      add(std::move(search->second));
      _buffer.erase(_current_index);
      _current_index++;
    }
    // at least one partial_result was added -> notify
    this->_cv->notify_one();
  } else {
    // buffer the partial result
    _buffer.insert({id, std::move(partial_result)});
  }
}

// _____________________________________________________________________________
size_t GrepOutput::size() const { return _lines_written; }

// _____________________________________________________________________________
void GrepOutput::add(std::vector<Grep::Match> partial_result) {
  INLINE_BENCHMARK_WALL_START(_, "output");
  for (auto& r : partial_result) {
    if (_options.line_number) {
      if (_options.color == Grep::Color::ON) {
        _ostream << GREEN << r.line_number << CYAN << ':' << COLOR_RESET;
      } else {
        _ostream << r.line_number << ':';
      }
    }
    if (_options.byte_offset) {
      if (_options.color == Grep::Color::ON) {
        _ostream << GREEN << r.byte_position << CYAN << ':' << COLOR_RESET;
      } else {
        _ostream << r.byte_position << ':';
      }
    }
    if (_options.only_matching) {
      if (_options.color == Grep::Color::ON) {
        _ostream << RED << r.match << COLOR_RESET << '\n';
      } else {
        _ostream << r.match << '\n';
      }
    } else {
      if (_options.color == Grep::Color::ON) {
        // search for every occurrence of pattern within the string and
        // print it out colored while the rest is printed uncolored.
        size_t shift = 0;
        size_t match_size = _options.pattern.size();
        while (true) {
          size_t match_pos;
          if (xs::utils::use_str_as_regex(_options.pattern) ||
              (_options.locale == Grep::Locale::UTF_8 &&
               _options.ignore_case)) {
            re2::RE2 re_pattern(
                '(' +
                std::string(_options.fixed_string
                                ? xs::utils::str::escaped(_options.pattern)
                                : _options.pattern) +
                ')');
            re2::StringPiece input(r.match.data() + shift,
                                   r.match.size() - shift);
            re2::StringPiece re_match;
            auto tmp = re2::RE2::PartialMatch(input, re_pattern, &re_match);
            if (tmp) {
              match_pos = re_match.data() - input.data() + shift;
              match_size = re_match.size();
            } else {
              break;
            }
          } else {
            const char* match;
            if (_options.ignore_case) {
              match = xs::search::simd::strcasestr(
                  r.match.data() + shift, r.match.size() - shift,
                  _options.pattern.data(), _options.pattern.size());
            } else {
              match = xs::search::simd::strstr(
                  r.match.data() + shift, r.match.size() - shift,
                  _options.pattern.data(), _options.pattern.size());
            }
            if (match == nullptr) {
              break;
            }
            match_pos = match - r.match.data();
          }
          // print string part uncolored (eq. pythonic substr is
          //  str[shift:match_pos]) and pattern in RED
          _ostream << std::string(
                          r.match.begin() + static_cast<int64_t>(shift),
                          r.match.begin() + static_cast<int64_t>(match_pos))
                   << RED << std::string(r.match.data() + match_pos, match_size)
                   << COLOR_RESET;
          // start next search at new shift
          shift = match_pos + match_size;
          if (shift >= r.match.size()) {
            break;
          }
        }
        // print rest of the string (eq. pythonic substr is str[shift:])
        _ostream << std::string(r.match.begin() + static_cast<int64_t>(shift),
                                r.match.end())
                 << '\n';
      } else {
        _ostream << r.match << '\n';
      }
    }
  }
}
