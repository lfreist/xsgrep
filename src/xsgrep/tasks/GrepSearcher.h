// Copyright 2023, Leon Freist
// Author: Leon Freist <freist@informatik.uni-freiburg.de>

#pragma once

#include "../grep.h"
#include "./GrepOutput.h"

/**
 * GrepSearcher: The searcher used by the xs::Executor for searching results.
 */
class GrepSearcher
    : public xs::task::base::ReturnProcessor<xs::DataChunk,
                                             std::vector<Grep::Match>> {
 public:
  /**
   * @param options: search/output options for grep like results
   */
  GrepSearcher(std::string pattern, bool byte_offset, bool line_number,
                        bool match_only, bool regex, bool ignore_case, Grep::Locale locale);

  /**
   * Search provided data according to the specified search criteria using a
   *  plain text pattern
   * @param pattern: plain text pattern
   * @param data: data that are searched
   * @return
   */
  std::vector<Grep::Match> process(xs::DataChunk* data) const override;

 private:
  std::vector<Grep::Match> process_regex(xs::DataChunk* data) const;
  std::vector<Grep::Match> process_plain(xs::DataChunk* data) const;

  /// search for line numbers
  std::string _pattern;
  bool _line_number;
  bool _byte_offset;
  bool _only_matching;
  bool _regex;
  bool _ignore_case;
  Grep::Locale _locale;
  std::unique_ptr<re2::RE2> _re_pattern;
};
