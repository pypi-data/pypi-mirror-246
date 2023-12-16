
        message(WARNING "Using `SPIRVTargets.cmake` is deprecated: use `find_package(glslang)` to find glslang CMake targets.")

        if (NOT TARGET glslang::SPIRV)
            include("${PACKAGE_PREFIX_DIR}/lib/cmake/glslang/glslang-targets.cmake")
        endif()

        add_library(SPIRV ALIAS glslang::SPIRV)
    