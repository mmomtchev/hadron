cmake_minimum_required(VERSION 3.5)

project(cmMod)
set (CMAKE_CXX_STANDARD 14)


add_library(cmModLib++ ${DEFAULT_LIBRARY} cmMod.cpp)
target_compile_definitions(cmModLib++ PRIVATE CMMODXX_BUILD ${DEFAULT_LIBRARY})

add_library(cmModLibInternal ${DEFAULT_LIBRARY} cmMod_internal.cpp)
target_compile_definitions(cmModLibInternal PRIVATE CMMODINTERNAL_BUILD ${DEFAULT_LIBRARY})

target_link_libraries(cmModLib++ PUBLIC cmModLibInternal)
