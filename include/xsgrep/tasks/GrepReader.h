// Copyright 2023, Leon Freist
// Author: Leon Freist <freist@informatik.uni-freiburg.de>

#pragma once

#include <xsearch/tasks/base/DataProvider.h>
#include <xsearch/tasks/defaults/readers.h>
#include <xsearch/DataChunk.h>

#include <queue>
#include <filesystem>

using namespace xs;


class GrepReader : public task::base::DataProvider<DataChunk> {
 public:
  explicit GrepReader(std::string path, int recursive_depth = -1);

  std::optional<std::pair<DataChunk, chunk_index>> getNextData() override;

 private:
  bool getNextFiles();
  std::queue<std::pair<std::filesystem::path, int>> _directory_queue;
  std::queue<std::filesystem::path> _file_queue;
  std::unique_ptr<task::reader::FileReader<DataChunk>> _reader;
  int _recursive_depth;
  uint64_t _chunk_index{0};
};