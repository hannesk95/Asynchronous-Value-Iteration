# Install script for directory: /mnt/c/Users/Johan/Documents/GIT/Asynchronous-Value-Iteration/cpp_backend/lib

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Debug")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/mnt/c/Users/Johan/Documents/GIT/Asynchronous-Value-Iteration/cpp_backend/../backend/inc")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/mnt/c/Users/Johan/Documents/GIT/Asynchronous-Value-Iteration/cpp_backend/../backend" TYPE DIRECTORY MESSAGE_NEVER FILES "/mnt/c/Users/Johan/Documents/GIT/Asynchronous-Value-Iteration/cpp_backend/lib/inc" FILES_MATCHING REGEX "/[^/]*$")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
    if(EXISTS "$ENV{DESTDIR}/mnt/c/Users/Johan/Documents/GIT/Asynchronous-Value-Iteration/cpp_backend/../backend/lib/libbackend.so" AND
       NOT IS_SYMLINK "$ENV{DESTDIR}/mnt/c/Users/Johan/Documents/GIT/Asynchronous-Value-Iteration/cpp_backend/../backend/lib/libbackend.so")
      file(RPATH_CHECK
           FILE "$ENV{DESTDIR}/mnt/c/Users/Johan/Documents/GIT/Asynchronous-Value-Iteration/cpp_backend/../backend/lib/libbackend.so"
           RPATH "")
    endif()
    list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
     "/mnt/c/Users/Johan/Documents/GIT/Asynchronous-Value-Iteration/cpp_backend/../backend/lib/libbackend.so")
    if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
        message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
    endif()
    if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
        message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
    endif()
file(INSTALL DESTINATION "/mnt/c/Users/Johan/Documents/GIT/Asynchronous-Value-Iteration/cpp_backend/../backend/lib" TYPE SHARED_LIBRARY FILES "/mnt/c/Users/Johan/Documents/GIT/Asynchronous-Value-Iteration/cpp_backend/cmake-build-debug/lib/libbackend.so")
    if(EXISTS "$ENV{DESTDIR}/mnt/c/Users/Johan/Documents/GIT/Asynchronous-Value-Iteration/cpp_backend/../backend/lib/libbackend.so" AND
       NOT IS_SYMLINK "$ENV{DESTDIR}/mnt/c/Users/Johan/Documents/GIT/Asynchronous-Value-Iteration/cpp_backend/../backend/lib/libbackend.so")
      if(CMAKE_INSTALL_DO_STRIP)
        execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/mnt/c/Users/Johan/Documents/GIT/Asynchronous-Value-Iteration/cpp_backend/../backend/lib/libbackend.so")
      endif()
    endif()
  endif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
  endif("${CMAKE_INSTALL_CONFIG_NAME}" MATCHES "^([Rr][Ee][Ll][Ee][Aa][Ss][Ee])$")
endif()

