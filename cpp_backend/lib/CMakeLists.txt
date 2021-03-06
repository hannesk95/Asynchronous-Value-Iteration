# A shared library for the Python Code
cmake_minimum_required (VERSION 3.0)

# Set the name for the case this CMakeLists.txt is used directly.
# A description of the variables is given in the top level CMakeLists
# Typically, you want to work with the outer CMakeLists.txt
if(NOT DEFINED LIB_NAME)
  set(LIB_NAME backend)
  set(DEST_LIB "${PROJECT_SOURCE_DIR}/install/lib")
  set(DEST_INC "${PROJECT_SOURCE_DIR}/install/")
endif()

# Additional 'find module' scipts in the subfolder 'cmake'
# Currently, FindLAPACKE is the important one. FindMKL exist for the case that you need it in another project.
set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/cmake/;${CMAKE_MODULE_PATH}")

# We want parallel code later-on ...
find_package(OpenMP REQUIRED)

# Basic Linear Algebra Subprogram (BLAS): description of fastest elementary matrix / vector operations
# The Fortran realization of BLAS is provided by 'OpenBlas', and should be the fastest implementation
# without vendor lock.
#
# Intel's Math Kerner Library (MKL) is normally the best choice for even faster linear algebra code,
# but as the name suggests it is not available on AMD Machines. Also our HPC CPUs are too old ...
#
# Capital letters required here and in the following, I learned it the hard way ...
find_package(BLAS REQUIRED)    

# The Linear Algebra Package (LAPACK) makes use of the operations defined in BLAS to provide the actual 
# linear algebra stuff (e.g. equation solver or SVD), Numpy also uses it in the background.
#
# OpenLapack provides the implementation similar to OpenBlas, Intel MKL would be faster and has everything
# included (BLAS + LAPACK + OpenMP), but Intel is greedy and restricts it to their CPUs ...
find_package(LAPACK REQUIRED)  

# Interface for Eigen between C++ and Fortran: 
# Eigen, a C++ library, requires some code to communicate with the Fortran implementation of BLAS and LAPACK
# Pay attention to the E in the end.
find_package(LAPACKE REQUIRED)

# Collect all source files for easy compilation
set(SRC_FILES ${CMAKE_CURRENT_LIST_DIR}/src/Iterator.cpp)

# The complete include folder, which is required for cffi to use the Interface.h
set(INC_DIR ${CMAKE_CURRENT_LIST_DIR}/inc)

# Add additional include directories for the backend:
# - eveything in our directory 'inc'
# - lib/ directory itself for sake of completeness (if we decide to place a header next to the CMakeLists.txt)
# - modules we need (mainly the optional requirements for eigen such as blas or lapack)
include_directories(${CMAKE_CURRENT_LIST_DIR}
                    ${CMAKE_CURRENT_LIST_DIR}/inc
                    ${LAPACKE_INCLUDE_DIRS_DEP} # = include directories of lapacke and dependencies 
                    )
                    
# Tell cmake where additional link directories are located
# We do not need this here, because the Find??? cmake files for LAPACK etc. already do this
#link_directories(${LAPACKE_LIBRARY_DIRS_DEP}) # link directories of lapacke + dependencies 

# This puts the code together into the library
add_library(${LIB_NAME} SHARED ${SRC_FILES})

# To check if LAPACKE LIBS with DEP suffix already include BLAS and normal LAPACK:
# message("LAPACKE_LIBRARIES_DEP: ${LAPACKE_LIBRARIES_DEP}")
# message("BLAS_LIBRARIES: ${BLAS_LIBRARIES}")
# message("LAPACK_LIBRARIES: ${LAPACK_LIBRARIES}")
#
# Result is something like:
# LAPACKE_LIBRARIES_DEP: /usr/lib/x86_64-linux-gnu/liblapacke.so;/usr/lib/x86_64-linux-gnu/libopenblas.so;/usr/lib/x86_64-linux-gnu/libopenblas.so;-lm
# BLAS_LIBRARIES: /usr/lib/x86_64-linux-gnu/libopenblas.so
# LAPACK_LIBRARIES: /usr/lib/x86_64-linux-gnu/libopenblas.so;/usr/lib/x86_64-linux-gnu/libopenblas.so
# For some reason LAPACK_LIBRARIES includes it twice
#
# Conclusion: LAPACKE_LIBRARIES_DEP is enough, everything is included
target_link_libraries(${LIB_NAME} OpenMP::OpenMP_CXX ${LAPACKE_LIBRARIES_DEP})

# Create 'make install' instruction to move required files in the python 'backend' folder
# We can use variables from the top level cmake file: DEST_INC and DEST_LIB are defined

if(WIN32)
  # Visual Studio does not like these instructions and spams error messages, hence this if else construction
  # Even if compilation does not work with this cmake file under windows you can still use Visual Studio 
  # and its code completion. (I'm using the full 2017 Enterprise Version, not VS Code)
  message("No install step for windows!")

else()

  # Tell cmake what belongs to the public header files and must be copied for the install target.
  # Different than before just copy the whole include folder, then we do not have to pay attention to flattened
  # folder hierarchies (take a look at the structure of Eigen, this must be preserved!)
  install(DIRECTORY ${INC_DIR} DESTINATION ${DEST_INC} MESSAGE_NEVER FILES_MATCHING PATTERN "*" )

  # Install target for the actual libary as before
  install(TARGETS ${LIB_NAME} LIBRARY DESTINATION ${DEST_LIB} CONFIGURATIONS Release)
endif()
