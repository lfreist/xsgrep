add_subdirectory(tasks)
add_subdirectory(xspp)

add_executable(xs Main.cpp)
target_link_libraries(xs PUBLIC GrepTasks boost_program_options)