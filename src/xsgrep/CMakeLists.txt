add_subdirectory(tasks)
add_library(libgrep grep.cpp)
target_link_libraries(libgrep PUBLIC GrepTasks)