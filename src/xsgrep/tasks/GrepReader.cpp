// Copyright 2023, Leon Freist
// Author: Leon Freist <freist@informatik.uni-freiburg.de>

#include <xsgrep/tasks/GrepReader.h>

#include <iostream>

GrepReader::GrepReader(std::string path, int recursive_depth)
    : task::base::DataProvider<DataChunk>(1),
      _recursive_depth(recursive_depth) {
  if (std::filesystem::is_regular_file(path)) {
    _file_queue.emplace(std::move(path));
  } else if (std::filesystem::is_directory(path)) {
    _directory_queue.emplace(std::move(path), 0);
  } else {
    throw std::runtime_error(path + " is not a file or directory.");
  }
}

std::optional<std::pair<DataChunk, chunk_index>> GrepReader::getNextData() {
  if (_reader == nullptr) {
    if (_file_queue.empty()) {
      if (getNextFiles()) {
        auto file = std::move(_file_queue.front());
        _file_queue.pop();
        _reader =
            std::make_unique<task::reader::FileBlockReader>(std::move(file));
      } else {
        // no files left, stop reading
        return {};
      }
    } else {
      auto file = std::move(_file_queue.front());
      _file_queue.pop();
      _reader =
          std::make_unique<task::reader::FileBlockReader>(std::move(file));
    }
  }
  auto res = _reader->getNextData();
  if (!res.has_value()) {
    _reader = nullptr;
    _chunk_index++;
    return getNextData();
  }
  _chunk_index += res->second;
  return {std::make_pair(res->first, res->second + _chunk_index)};
}

bool GrepReader::getNextFiles() {
  while (true) {
    if (_directory_queue.empty()) {
      // no additional files found, break and return false
      break;
    }
    // pop next directory from queue
    auto directory = std::move(_directory_queue.front());
    _directory_queue.pop();
    // skip directory if recursion depth is reached
    if (directory.second >= _recursive_depth && _recursive_depth != -1) {
      continue;
    }
    // iterate through all objects within the given directory
    for (auto& obj : std::filesystem::directory_iterator(directory.first)) {
      if (std::filesystem::is_regular_file(obj)) {
        // if object is file, add it to file queue
        _file_queue.push(obj);
      } else if (std::filesystem::is_directory(obj)) {
        // if object is directory add it to directory queue and increase
        // recursive counter
        _directory_queue.emplace(obj, directory.second + 1);
      }
    }
    // repeat if no files were added
    if (_file_queue.empty()) {
      continue;
    }
    return true;
  }
  return false;
}