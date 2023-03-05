#include <xsearch/xsearch.h>

int main(int argc, char** argv) {
  std::string a(argv[1]);
  std::cout << a << std::endl;
  xs::utils::str::simd::toLower(a.data(), a.size());
  std::cout << a << std::endl;
  return 0;
}