cmake_minimum_required(VERSION 3.10)
project(WraithCore)

set(CMAKE_CXX_STANDARD 14)

add_library(wraith_core STATIC
    wraith_core/src/relay.cpp
)

target_include_directories(wraith_core PUBLIC
    include
)

# Export for external projects
install(TARGETS wraith_core DESTINATION lib)
install(DIRECTORY include/wraith_core DESTINATION include)
