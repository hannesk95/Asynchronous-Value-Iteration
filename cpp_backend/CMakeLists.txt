cmake_minimum_required (VERSION 3.0)

# Compiler flags for all configuration, -Wall enables all warnings
set(CMAKE_CXX_FLAGS "-Wall")

# Flags for debug configuration: -g activates creation of debug information in executable
# set(CMAKE_CXX_FLAGS_DEBUG "-g")

# Flags for release configuration: 
# -O3:           level 3 compiler optimizations => faster code
# -march-native: compile for the native (=your computer) architecture => faster code
# -ffast-math:   allow "unsafe" match operations, i.e. those operations, where the result of a floating point operation could be unstable
#                This might be a problem for cross platform but deterministic applications (e.g. multiplayer games)
#                allow fast math => faster code
# -fopenmp:      activate openmp support (next lecture), might be enabled by default depending on your compiler
set(CMAKE_CXX_FLAGS_RELEASE "-O3 -march=native -ffast-math -fopenmp")

# The name for this library, let's be super creative and call it 'backend'
set(LIB_NAME backend)

# The name for the c++ test program (mainly for debugging with an IDE, the debugger needs an entry point to the library)
project(${LIB_NAME}.exe)

# The path required for installing the library, cmake moves the libbackend.so file in this folder
set(DEST_LIB ${PROJECT_SOURCE_DIR}/../backend/lib)

# The path for all headers belonging to the interface, no subfolder 'inc' because the full directory is copied,
# i.e. a folder 'inc' is created at the target location
set(DEST_INC ${PROJECT_SOURCE_DIR}/../backend)  

# To make use of the our library add a subdirectory call to build and install it
# -> no need to care about the library when using an IDE to "open" this CMakeLists.txt
add_subdirectory(lib)

# Avoid annoying paths in main.cpp by providing the additional include directories
include_directories(lib/inc)

# All additional source files for debugging, e.g. if the debugging code is located in different files
set(SRC_FILES main.cpp)

# Create an executable as usual, especially debugging C++ code with Qt becomes easy
add_executable(${PROJECT_NAME} ${SRC_FILES})

# Finally, link the executable against the library -> linker is happy
target_link_libraries(${PROJECT_NAME} ${LIB_NAME})
