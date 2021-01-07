from cffi import FFI


def compile_interface(verbose=True):
    """
  Use API mode of cffi to get speed of access and proper errors.

  This means you invoke

  >>> ffi.set_source(...)

  with headers and path to libraries followed by the compilation step

  >>> ffi.compile(verbose=True)
  
  which is started by importing the backend.
  """

    # The main FFI instance which we use to create the interface
    ffi = FFI()

    # More or less directly the content of interface.h, better would be to parse that file!
    # Use 3 quotes to format freely the C-Function and don't forget the ; in the end!

    ffi.cdef("""void cffi_iterate(double* data, int* indices, int* indptr, const unsigned int n_rows, 
                                const unsigned int n_columns, double* J_star, double* J, double* pi, double epsilon, 
                                double alpha, const unsigned int n_actions, const unsigned int n_stars, 
                                const unsigned int n_states, const unsigned int n_nonzero);""")

    # Now create the full glue code to your library
    ffi.set_source("cpp_interface",
                   # name of the output C/C++ extension, name is not important, but use something unique

                   # Header with the interface, the content must match the cdef's from above
                   #
                   # The content of that interface.h could also be defined here as python string, but the C-Include
                   # results in less duplicated code
                   """ #include "Interface.h" """,

                   # Additional include directories as list of strings, here only the public headers of the library
                   include_dirs=['inc'],

                   # includes pi.c as additional sources
                   # (we don't need this, your source code is already compiled as library)
                   # sources=['src/foo.c'],

                   # Our code is in a shared / static library, hence we have to link against it
                   # 'lib' prefix and '.so' suffix are already covered by ffi, so we put here just the name
                   # as specified in CMakeLists.txt
                   libraries=['backend'],

                   # 'make install' copies the library into this folder (located in the same directory as this script)
                   # Provide a list of string with extra lib directories
                   library_dirs=['lib'],

                   # rpath is there to add properly 'libbackend.so' to LD_LIBRARY_PATH without exporting by hand
                   # the directory as environment variable, i.e you can avoid to write something like
                   #
                   # >>> export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/.../backend/lib
                   #
                   # in your bashrc or everytime in the console.
                   #
                   # From the troubleshooting section of CFFI:
                   #
                   #   you can compile MODULENAME.so with the path hard-coded inside in the first place.
                   #   $ORIGIN is directory where MODULE_NAME.so is, i.e. the name directly after set_source(...)
                   #
                   # Hence, also add our 'lib' directory to $ORIGIN, then it works.
                   #
                   # Use the extra link args to inform the linker about openmp (for later)
                   extra_link_args=['-Wl,-rpath=$ORIGIN/lib', '-fopenmp'],

                   # To get a fast interface compile with optimizations (similar to CMakeLists.txt, look there for
                   # explanations)
                   #
                   # Currently I don't know how to get rid of default -O2 argument. If you look at the console output
                   # you will see both -O3 and -O2. I don't know what gcc does if both are specified (choosing highest or
                   # lowest, maybe using both?!)
                   #
                   # Nevertheless, the interface should not be the bottleneck, as it is just forwarding the pointers to
                   # the already compiled library.
                   extra_compile_args=['-O3', '-march=native', '-ffast-math', '-fopenmp', '-D use_openmp'],

                   # The ``source_extension`` keyword makes sure the C compiler treats it
                   # as C++.  The ``extern "C"`` part in the C++ code makes sure that the
                   # function name is not mangled in the compiled module.
                   source_extension='.cpp')

    return ffi.compile(verbose=verbose)


# You can use this python file directly to compile the interface
if __name__ == "__main__":
    compile_interface()
