cmake_minimum_required(VERSION 3.5)

project(subdir)

set(CMAKE_CXX_STANDARD 14)

add_library(explicit_libs INTERFACE)

if(WIN32)
  target_compile_definitions(explicit_libs INTERFACE WIN32)
  target_link_libraries(explicit_libs INTERFACE shell32.lib)
endif()
