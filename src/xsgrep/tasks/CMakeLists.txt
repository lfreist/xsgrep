add_library(GrepTasks GrepResult.cpp GrepSearcher.cpp)
target_link_libraries(GrepTasks PUBLIC xsearch)