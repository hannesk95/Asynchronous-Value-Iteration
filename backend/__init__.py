from . import backend_py

# Second name, which can be the cpp code whenever possible, but falls back to python if needed
backend = backend_py

try:
  # Hide python backend by overwriting the variable
  from . import backend_cpp as backend

  # Import python backend with original name (just in case it is still required)
  from . import backend_py

except (ModuleNotFoundError, ImportError) as e:
  import logging
  _logger = logging.getLogger(__name__)
  _logger.warning(f"The c++ backend could not be imported, falling back to python!\nReason:\n\n{e}\n\n")

  # Might be handy to kill the program if this step fails ...
  # print(f"Reason - {type(e)}:", e)
  # import sys
  # sys.exit(1)

# Only import important stuff with 'from backend import *'
__all__ = ["backend", "backend_py"]
