import os
import logging

_logger = logging.getLogger(__name__)


######################
#   Interface Part   #
######################

def _find_compile_output():
    """ Returns all the files that belong to the compiled interface """

    def should_include(bar):
        return bar.startswith("cpp_interface") and bar.endswith((".cpp", ".o", ".so"))

    return [foo for foo in os.listdir(os.path.dirname(__file__)) if should_include(foo)]


def _compile_output_complete():
    return len(_find_compile_output()) == 3


if not _compile_output_complete():
    _logger.warning("Only parts of the expected compilation output are present. Trying to compile the c++ backend now.")

    # This is the folder in which backend_cpp.py is located
    the_dir = os.path.dirname(__file__)

    # These are created during the 'make install' step
    inc_dir = os.path.join(the_dir, 'inc')
    lib_dir = os.path.join(the_dir, 'lib')

    if not os.path.exists(inc_dir) or not os.path.exists(lib_dir) or \
            len(os.listdir(inc_dir)) == 0 or \
            len(os.listdir(lib_dir)) == 0:
        raise ImportError("The include and/or library folder is not existing or empty, did you run 'make install'?")

    from .compile_interface import compile_interface

    # We must change into the folder with the compile script, otherwise the include folder is at the wrong location
    # Use the location of this python script as "robust" change directory instruction
    os.chdir(the_dir)

    compile_interface(verbose=True)

    # Now go back to the parent folder to not affect the remaining script
    # Since the working directory is now known it is enough to go one level up
    os.chdir("..")

if not _compile_output_complete():
    _logger.error("The expected compilation output is incomplete, stopping here!")
    raise ImportError("The compilation of the c++ python interface was not successful.")

try:
    # This is the name we set in set_source(...), i.e. the first argument
    from . import cpp_interface
    from cffi import FFI

except (ModuleNotFoundError, ImportError) as e:
    _logger.error(f"Compiled interface is present, yet importing failed.\nReason:\n\n{e}\n\n")
    raise

# For casting the pointers
_ffi = FFI()


#############################
# Wrappers for the c++ code #
#############################

def iterate(data, indices, indptr, n_rows, n_columns,
            J_star, J, pi, epsilon, alpha, n_actions,
            n_stars, n_states, n_nonzero):
    if n_states != len(J_star):
        raise ValueError("Missmatch between state values and states.")

    data_ptr = _ffi.cast("double*", data.ctypes.data)
    indices_ptr = _ffi.cast("int*", indices.ctypes.data)
    indptr_ptr = _ffi.cast("int*", indptr.ctypes.data)
    J_star_ptr = _ffi.cast("double*", J_star.ctypes.data)
    J_ptr = _ffi.cast("double*", J.ctypes.data)
    pi_ptr = _ffi.cast("double*", pi.ctypes.data)

    cpp_interface.lib.cffi_iterate(data_ptr, indices_ptr, indptr_ptr, n_rows, n_columns,
                                   J_star_ptr, J_ptr, pi_ptr, epsilon, alpha, n_actions,
                                   n_stars, n_states, n_nonzero)

    return J, pi