// Copyright 2023, Leon Freist
// Author: Leon Freist <freist@informatik.uni-freiburg.de>

#include <xsearch/utils/string_utils.h>
#include <xsgrep/grep.h>
#include <xsgrep/tasks/GrepReader.h>
#include <xsgrep/tasks/GrepResult.h>
#include <xsgrep/tasks/GrepSearcher.h>

// ===== Helper functions ======================================================
/**
 * Helper function that recursively traverses directories and returns a list of
 *  all files.
 * @param in_path
 * @param files
 * @param depth
 */
void get_files_recursive(const std::filesystem::path& in_path,
                         std::vector<std::string>* files, int depth) {
  if (std::filesystem::is_regular_file(in_path)) {
    files->push_back(std::filesystem::path(in_path));
  }
  if (depth == 0) {
    return;
  }
  if (std::filesystem::is_directory(in_path)) {
    for (auto& obj : std::filesystem::directory_iterator(in_path)) {
      get_files_recursive(obj, files, depth - 1);
    }
  }
}

/**
 * Get a vector of all files within a directory
 * @param in_path start directory
 * @param max_depth recursion depth
 * @return
 */
std::vector<std::string> get_files(const std::filesystem::path& in_path,
                                   int max_depth) {
  if (in_path.empty() || in_path == "-") {
    return {"-"};
  }
  std::vector<std::string> files;
  get_files_recursive(in_path, &files, max_depth);
  return files;
}
// =============================================================================

Grep::Grep(std::string pattern, std::string file) {
  _options.pattern = std::move(pattern);
  set_file(std::move(file));
}

Grep::Grep(Options options) : _options(std::move(options)) {
  // these three members need to be set using setter method in case they are set
  //  to default values
  set_colored_output(_options.color);
  set_num_threads(_options.num_threads);
  set_locale(_options.locale);
  set_num_reader_threads(_options.num_reader_threads);
  set_file(_options.file);
}

std::vector<std::pair<std::string, uint64_t>> Grep::count() {
  std::vector<std::pair<std::string, uint64_t>> result;
  for (const auto& file : get_files(_options.file)) {
    auto executor =
        xs::Executor<xs::DataChunk, xs::result::base::CountResult, uint64_t>(
            _options.num_threads, get_reader(file), get_processors(),
            std::make_unique<xs::task::searcher::LineCounter>(
                _options.pattern, use_regex(), _options.ignore_case,
                _options.locale == Grep::Locale::UTF_8),
            std::make_unique<xs::result::base::CountResult>());
    executor.join();
    result.emplace_back(file, executor.getResult()->size());
  }
  return result;
}

std::map<std::string, std::vector<Grep::Match>> Grep::search() {
  auto executor =
      xs::Executor<xs::DataChunk, GrepContainer,
                   std::pair<std::string, std::vector<Grep::Match>>>(
          _options.num_threads, get_reader(_options.file), get_processors(),
          std::make_unique<GrepSearcher>(_options.pattern, _options.byte_offset,
                                         _options.line_number,
                                         _options.only_matching, use_regex(),
                                         _options.ignore_case, _options.locale),
          std::make_unique<GrepContainer>());
  executor.join();
  return executor.getResult()->copyResultSafe();
}

void Grep::write(std::ostream* stream) {
  if (_options.count) {
    for (const auto& res : count()) {
      if (_options.print_file_path) {
        if (_options.color == Grep::Color::ON) {
          *stream << MAGENTA << res.first << CYAN << ':';
        } else {
          *stream << res.first << ':';
        }
      }
      *stream << res.second << '\n';
    }
  } else {
    if (!(_options.file.empty() || _options.file == "-" ||
          std::filesystem::is_regular_file(_options.file) ||
          std::filesystem::is_directory(_options.file))) {
      std::cerr << _options.file << ": No such file or directory\n";
      return;
    }
    auto executor =
        xs::Executor<xs::DataChunk, GrepOutput,
                     std::pair<std::string, std::vector<Grep::Match>>,
                     Grep::Options, std::ostream&>(
            _options.num_threads, get_reader(_options.file), get_processors(),
            std::make_unique<GrepSearcher>(
                _options.pattern, _options.byte_offset, _options.line_number,
                _options.only_matching, use_regex(), _options.ignore_case,
                _options.locale),
            std::make_unique<GrepOutput>(_options, *stream));
    executor.join();
  }
}

Grep& Grep::set_file(std::string file) {
  _options.file = std::move(file);
  if (std::filesystem::is_directory(_options.file)) {
    _options.print_file_path = true;
  }
  return *this;
}

Grep& Grep::set_meta_file(std::string meta_file) {
  _options.meta_file_path = std::move(meta_file);
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
  int fallback_value = _max_phys_cores / 2;
  if (fallback_value < 2) {
    fallback_value = 2;
  }
  if (_options.num_threads > 0) {
    _options.num_threads = val > _max_phys_cores ? _max_phys_cores : val;
  } else if (_options.num_threads == 0) {
    _options.num_threads = fallback_value;
  } else {  // < 0
    _options.num_threads = _max_phys_cores;
  }
  return *this;
}

Grep& Grep::set_num_reader_threads(int val) {
  _options.num_reader_threads =
      val <= 1 ? 1 : (val > _max_phys_cores ? _max_phys_cores : val);
  return *this;
}

const std::string& Grep::file() const { return _options.file; }

const std::string& Grep::meta_file() const { return _options.meta_file_path; }

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

int Grep::num_reader_threads() const { return _options.num_reader_threads; }

// ----- private ---------------------------------------------------------------
std::vector<Grep::base_processors> Grep::get_processors() const {
  std::vector<std::unique_ptr<xs::task::base::InplaceProcessor<xs::DataChunk>>>
      ret;
  if (_options.meta_file_path.empty()) {
    if (_options.line_number) {
      ret.push_back(std::make_unique<xs::task::processor::NewLineSearcher>());
    }
  } else {
    xs::MetaFile metaFile(_options.meta_file_path, std::ios::in);
    switch (metaFile.get_compression_type()) {
      case xs::CompressionType::LZ4:
        ret.push_back(std::make_unique<xs::task::processor::LZ4Decompressor>());
        break;
      case xs::CompressionType::ZSTD:
        ret.emplace_back(
            std::make_unique<xs::task::processor::ZSTDDecompressor>());
        break;
      default:
        break;
    }
  }
  return ret;
}

Grep::base_reader Grep::get_reader(const std::string& file) {
  if (std::filesystem::is_directory(_options.file)) {
    return std::make_unique<GrepReader>(_options.file);
  }
  if (file.empty() || file == "-") {
    return std::make_unique<xs::task::reader::FileBlockReader>("/dev/stdin");
  }
  if (_options.meta_file_path.empty()) {
    if (_options.no_mmap) {
      return std::make_unique<xs::task::reader::FileBlockReader>(file);
    }
    return std::make_unique<xs::task::reader::FileBlockReaderMMAP>(file);
  } else {
    if (_options.num_reader_threads == 1) {
      return std::make_unique<xs::task::reader::FileBlockMetaReaderSingle>(
          file, _options.meta_file_path);
    }
    if (_options.no_mmap) {
      return std::make_unique<xs::task::reader::FileBlockMetaReader>(
          file, _options.meta_file_path, _options.num_reader_threads);
    } else {
      return std::make_unique<xs::task::reader::FileBlockMetaReaderMMAP>(
          file, _options.meta_file_path, _options.num_reader_threads);
    }
  }
}

bool Grep::use_regex() const {
  return xs::utils::use_str_as_regex(_options.pattern) &&
         !_options.fixed_string;
}

const int Grep::_max_phys_cores =
    static_cast<int>(std::thread::hardware_concurrency()) / 2;
