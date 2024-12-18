cmake_minimum_required(VERSION 3.10)
project(lab3_os LANGUAGES NONE)

find_package(Python3 COMPONENTS Interpreter REQUIRED)
set(PYTHON_SCRIPT "${CMAKE_CURRENT_SOURCE_DIR}/script.py")

add_custom_target(run
    COMMAND ${Python3_EXECUTABLE} ${PYTHON_SCRIPT}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMENT "Running the Python script..."
)

