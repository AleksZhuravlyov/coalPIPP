cmake_minimum_required(VERSION 3.14)

project(coalPIP)

set(CMAKE_CXX_STANDARD 17)

find_package(pybind11 REQUIRED)

find_package(Eigen3 REQUIRED)

include_directories(
        numerical/equation
        numerical/math)


pybind11_add_module(cfd
        numerical/wrapper.cpp
        numerical/equation/Equation.cpp
        numerical/equation/Steady.cpp
        numerical/equation/Transient.cpp
        numerical/math/Props.cpp
        numerical/math/Local.cpp
        numerical/math/Convective.cpp)


target_include_directories(cfd PUBLIC ${EIGEN3_INCLUDE_DIRS})

target_link_libraries(cfd ${EIGEN3_LIBRARIES})

set_target_properties(cfd PROPERTIES LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/../numerical)

