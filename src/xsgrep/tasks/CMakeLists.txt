add_library(GrepTasks GrepReader.cpp GrepResult.cpp GrepSearcher.cpp)
target_link_libraries(GrepTasks PUBLIC xsearch)