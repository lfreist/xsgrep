add_subdirectory(tasks)

add_executable(xs main.cpp)
target_link_libraries(xs PUBLIC GrepTasks boost_program_options)