cmake_minimum_required(VERSION 3.5)
# Create a "compile_commands.json" file to inform LSP about build configuration
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
# specify the C++ standard:
set(CMAKE_CXX_STANDARD 20)
if (WIN32)
    set(VCPKG_TARGET_TRIPLET "x64-windows")
elseif (APPLE)
    set(VCPKG_TARGET_TRIPLET "arm64-osx")
else ()
    message(FATAL_ERROR "Platform not supported: supported platforms are 64-bit windows or mac-os, to compile for another platform edit the CMakeLists.txt file")
endif ()


# Set the vcpkg toolchain (make sure this is set before the `project()` call)
set(CMAKE_TOOLCHAIN_FILE "${CMAKE_CURRENT_SOURCE_DIR}/vcpkg/scripts/buildsystems/vcpkg.cmake"
    CACHE STRING "Vcpkg toolchain file")

project(Tessy)

# This is generally not needed if vcpkg toolchain is used correctly
set(OpenCV_DIR "${CMAKE_CURRENT_SOURCE_DIR}/vcpkg/packages/opencv4_x64-osx/share/opencv4")
set(quirc_DIR "${CMAKE_CURRENT_SOURCE_DIR}/vcpkg/packages/quirc_x64-osx/share/quirc")
set(Tesseract_DIR "${CMAKE_CURRENT_SOURCE_DIR}/vcpkg/installed/x64-osx/share/tesseract")
set(Leptonica_DIR "${CMAKE_CURRENT_SOURCE_DIR}/vcpkg/installed/x64-osx/share/leptonica")
set(LibArchive_DIR "${CMAKE_CURRENT_SOURCE_DIR}/vcpkg/installed/x64-osx/share/libarchive")

# Find packages
find_package(OpenCV REQUIRED)
find_package(Tesseract CONFIG REQUIRED)
find_package(quirc CONFIG REQUIRED)
find_package(Leptonica CONFIG REQUIRED)
find_package(LibArchive CONFIG REQUIRED)

# Include directories
include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(${Tesseract_INCLUDE_DIRS})

# Add an executable
add_executable(Tessy src/main.cpp)

# Manually set LibArchive directories
find_path(LIBARCHIVE_INCLUDE_DIR NAMES archive.h PATHS "${CMAKE_CURRENT_SOURCE_DIR}/vcpkg/installed/x64-osx/include")
find_library(LIBARCHIVE_LIBRARY NAMES archive PATHS "${CMAKE_CURRENT_SOURCE_DIR}/vcpkg/installed/x64-osx/lib")

message("LibArchive include directory: ${LibArchive_INCLUDE_DIR}")
message("LibArchive library: ${LibArchive_LIBRARY}")

# Include OpenCV headers
include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(${LIBARCHIVE_INCLUDE_DIR})

# Link libraries
target_link_libraries(Tessy PRIVATE ${OpenCV_LIBS} Tesseract::libtesseract leptonica quirc::quirc ${LibArchive_LIBRARY})
