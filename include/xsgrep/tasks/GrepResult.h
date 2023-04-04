// Copyright 2023, Leon Freist
// Author: Leon Freist <freist@informatik.uni-freiburg.de>

#pragma once

#include <unistd.h>
#include <xsearch/xsearch.h>

#include <cstdio>
#include <memory>

#include "../grep.h"

// ===== Output colors =========================================================
#define COLOR_RESET "\033[0m"
#define BLACK "\033[30m"              /* Black */
#define RED "\033[31m"                /* Red */
#define GREEN "\033[32m"              /* Green */
#define YELLOW "\033[33m"             /* Yellow */
#define BLUE "\033[34m"               /* Blue */
#define MAGENTA "\033[35m"            /* Magenta */
#define CYAN "\033[36m"               /* Cyan */
#define WHITE "\033[37m"              /* White */
#define BOLDBLACK "\033[1m\033[30m"   /* Bold Black */
#define BOLDRED "\033[1m\033[31m"     /* Bold Red */
#define BOLDGREEN "\033[1m\033[32m"   /* Bold Green */
#define BOLDYELLOW "\033[1m\033[33m"  /* Bold Yellow */
#define BOLDBLUE "\033[1m\033[34m"    /* Bold Blue */
#define BOLDMAGENTA "\033[1m\033[35m" /* Bold Magenta */
#define BOLDCYAN "\033[1m\033[36m"    /* Bold Cyan */
#define BOLDWHITE "\033[1m\033[37m"   /* Bold White */
// _____________________________________________________________________________

/**
 * GrepOutput: The actual result class that inherits xs::BaseResult.
 *  It collects vectors of GrepPartialResults.
 */
class GrepOutput : public xs::result::base::Result<std::vector<Grep::Match>> {
 public:
  explicit GrepOutput(Grep::Options options, std::ostream& ostream = std::cout);

  /**
   * Collect results and pass them ordered to the private add method.
   *  Results that are received before they are in turn are buffered in a
   *  std::map until its their turn.
   *
   * @param partial_result:
   * @param id: used for ordered output. Must be a closed sequence {0..X} of int
   */
  void add(std::vector<Grep::Match> partial_result, uint64_t id) override;

  /**
   * Return the number of lines written to ostream so far.
   *
   * @return:
   */
  size_t size() const override;

 private:
  /**
   * The actual output of the collected results. Called from public add method.
   *  Always writes to standard out.
   * @param partial_result
   */
  void add(std::vector<Grep::Match> partial_result) override;

  /// called by add for colored or uncolored output depending on _options.color
  void colored(std::vector<Grep::Match>& partial_result);
  void uncolored(std::vector<Grep::Match>& partial_result);

  Grep::Options _options;
  std::ostream& _ostream;

  /// Buffer for results that are received not in order
  std::unordered_map<uint64_t, std::vector<Grep::Match>> _buffer{};
  /// Indicates the index of the result that is written next
  uint64_t _current_index{0};
  uint64_t _lines_written{0};
};

class GrepContainer : public xs::result::base::ContainerResult<Grep::Match> {
 public:
  GrepContainer() = default;

  void add(std::vector<Grep::Match> partial_result, uint64_t id) override;
  void add(std::vector<Grep::Match> partial_result) override;

 private:
  /// Buffer for results that are received not in order
  std::unordered_map<uint64_t, std::vector<Grep::Match>> _buffer{};
  /// Indicates the index of the result that is written next
  uint64_t _current_index{0};
};