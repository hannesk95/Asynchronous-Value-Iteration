all:
	echo "Target all does nothing on its own"

clean: remove_interface remove_backend remove_pycache

remove_interface:
	rm -f cpp_interface.cpp
	rm -f cpp_interface.cpython-*.so
	rm -f cpp_interface.o

remove_backend:
	rm -rf inc
	rm -rf lib

remove_pycache:
	rm -rf __pycache__
