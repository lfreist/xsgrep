add_subdirectory(tasks)
add_library(libgrep grep.cpp)
target_link_libraries(libgrep PUBLIC GrepTasks)

add_executable(xs main.cpp)
target_link_libraries(xs PUBLIC libgrep boost_program_options)