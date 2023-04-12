// Copyright 2023, Leon Freist
// Author: Leon Freist <freist@informatik.uni-freiburg.de>

#include <gtest/gtest.h>
#include <xsgrep/tasks/GrepSearcher.h>

static const xs::DataChunk data(
    "This is a sample datachunk object\nwith Sherlock\nand She lock.", 61,
    {0, 0, 0, 61, 61, {{0, 0}}});

TEST(GrepSearcherTest, process_literal) {
  std::string pattern("Sherlock");
  {
    GrepSearcher searcher(pattern, false, false, false, false, false,
                          Grep::Locale::ASCII);
    auto res = searcher.process(&data);
    ASSERT_TRUE(res.first.empty());
    ASSERT_EQ(res.second.size(), 1);
    ASSERT_EQ(res.second.front().line_number, -1);
    ASSERT_EQ(res.second.front().byte_position, -1);
    ASSERT_EQ(res.second.front().match, "with Sherlock");
  }
  {
    GrepSearcher searcher(pattern, true, false, false, false, false,
                          Grep::Locale::ASCII);
    auto res = searcher.process(&data);
    ASSERT_TRUE(res.first.empty());
    ASSERT_EQ(res.second.size(), 1);
    ASSERT_EQ(res.second.front().line_number, -1);
    ASSERT_EQ(res.second.front().byte_position, 34);
    ASSERT_EQ(res.second.front().match, "with Sherlock");
  }
  {
    GrepSearcher searcher(pattern, false, true, false, false, false,
                          Grep::Locale::ASCII);
    auto res = searcher.process(&data);
    ASSERT_TRUE(res.first.empty());
    ASSERT_EQ(res.second.size(), 1);
    ASSERT_EQ(res.second.front().line_number, 2);
    ASSERT_EQ(res.second.front().byte_position, -1);
    ASSERT_EQ(res.second.front().match, "with Sherlock");
  }
  {
    GrepSearcher searcher(pattern, true, true, false, false, false,
                          Grep::Locale::ASCII);
    auto res = searcher.process(&data);
    ASSERT_TRUE(res.first.empty());
    ASSERT_EQ(res.second.size(), 1);
    ASSERT_EQ(res.second.front().line_number, 2);
    ASSERT_EQ(res.second.front().byte_position, 34);
    ASSERT_EQ(res.second.front().match, "with Sherlock");
  }
}

TEST(GrepSearcherTest, process_regex) {
  std::string pattern("She[r ]lock");
  {
    GrepSearcher searcher(pattern, false, false, false, true, false,
                          Grep::Locale::ASCII);
    auto res = searcher.process(&data);
    ASSERT_TRUE(res.first.empty());
    ASSERT_EQ(res.second.size(), 2);
    ASSERT_EQ(res.second.front().line_number, -1);
    ASSERT_EQ(res.second.front().byte_position, 34);
    ASSERT_EQ(res.second.front().match, "with Sherlock");
    ASSERT_EQ(res.second.back().line_number, -1);
    ASSERT_EQ(res.second.back().byte_position, 48);
    ASSERT_EQ(res.second.back().match, "and She lock.");
  }
  {
    GrepSearcher searcher(pattern, true, false, false, true, false,
                          Grep::Locale::ASCII);
    auto res = searcher.process(&data);
    ASSERT_TRUE(res.first.empty());
    ASSERT_EQ(res.second.size(), 2);
    ASSERT_EQ(res.second.front().line_number, -1);
    ASSERT_EQ(res.second.front().byte_position, 34);
    ASSERT_EQ(res.second.front().match, "with Sherlock");
    ASSERT_EQ(res.second.back().line_number, -1);
    ASSERT_EQ(res.second.back().byte_position, 48);
    ASSERT_EQ(res.second.back().match, "and She lock.");
  }
  {
    GrepSearcher searcher(pattern, false, true, false, true, false,
                          Grep::Locale::ASCII);
    auto res = searcher.process(&data);
    ASSERT_TRUE(res.first.empty());
    ASSERT_EQ(res.second.size(), 2);
    ASSERT_EQ(res.second.front().line_number, 2);
    ASSERT_EQ(res.second.front().byte_position, 34);
    ASSERT_EQ(res.second.front().match, "with Sherlock");
    ASSERT_EQ(res.second.back().line_number, 3);
    ASSERT_EQ(res.second.back().byte_position, 48);
    ASSERT_EQ(res.second.back().match, "and She lock.");
  }
  {
    GrepSearcher searcher(pattern, true, true, false, true, false,
                          Grep::Locale::ASCII);
    auto res = searcher.process(&data);
    ASSERT_TRUE(res.first.empty());
    ASSERT_EQ(res.second.size(), 2);
    ASSERT_EQ(res.second.front().line_number, 2);
    ASSERT_EQ(res.second.front().byte_position, 34);
    ASSERT_EQ(res.second.front().match, "with Sherlock");
    ASSERT_EQ(res.second.back().line_number, 3);
    ASSERT_EQ(res.second.back().byte_position, 48);
    ASSERT_EQ(res.second.back().match, "and She lock.");
  }
}