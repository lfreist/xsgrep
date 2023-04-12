cmake_minimum_required(VERSION 3.9)
project(xs LANGUAGES C CXX VERSION 1.0.0 DESCRIPTION "A GNU grep-like executable written with x-search")

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED 20)

set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -pedantic -Wno-unused-parameter")

find_package(Boost 1.74 REQUIRED COMPONENTS program_options)
include_directories(${Boost_INCLUDE_DIR})

add_subdirectory(x-search)
include_directories(x-search/include)

set(MAIN_PROJECT OFF)
if (CMAKE_CURRENT_SOURCE_DIR STREQUAL CMAKE_SOURCE_DIR)
    set(MAIN_PROJECT ON)
endif ()

include_directories(include)
add_subdirectory(src)

IF (${MAIN_PROJECT})
    # --- GTEST --------------------------------------------------------------------------------------------------------
    add_subdirectory(third_party/googletest)
    include_directories(third_party/googletest/googletest/include)
    # --- BOOST --------------------------------------------------------------------------------------------------------
    find_package(Boost 1.74 REQUIRED COMPONENTS program_options)
    include_directories(${Boost_INCLUDE_DIR})
    # ------------------------------------------------------------------------------------------------------------------
    add_executable(xspp xspp.cpp)
    target_link_libraries(xspp PUBLIC xspp_tasks boost_program_options)

    add_executable(xs xs.cpp)
    target_link_libraries(xs PUBLIC libgrep boost_program_options)

    add_executable(just_read src/benchutil/just_read.cpp)

    include(CTest)
    add_subdirectory(test)

    add_test(GrepSearcher test/src/tasks/GrepSearcherTestMain)
endif ()