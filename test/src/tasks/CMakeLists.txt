add_executable(GrepSearcherTestMain GrepSearcherTest.cpp)
target_link_libraries(GrepSearcherTestMain PUBLIC libgrep gtest_main)

add_executable(GrepResultTestMain GrepResultTest.cpp)
target_link_libraries(GrepResultTestMain PUBLIC libgrep gtest_main)

add_executable(GrepReaderTestMain GrepReaderTest.cpp)
target_link_libraries(GrepReaderTestMain PUBLIC libgrep gtest_main)