TARNAME = the_hpcmi_code.tar.gz
HOST = hpc06

all:
	@echo "This is a dummy to prevent running make without explicit target!"

clean: remove_pycharm
	$(MAKE) -C backend/ clean
	$(MAKE) -C cpp_backend/ clean
	$(MAKE) -C tests/ clean
	rm -rf .pytest_cache 

pack: clean
	rm -f $(TARNAME)
	tar -czf $(TARNAME) backend/ cpp_backend/ tests/ Makefile particles.py

unpack:
	tar -xzf $(TARNAME) 

send: pack
	scp $(TARNAME) $(HOST):~/Projects/hpcmi/

compile:
	$(MAKE) -C cpp_backend/ compile

test:
	python3 -m pytest tests/

remove_interface:
	$(MAKE) -C backend/ remove_interface

remove_pycharm:
	rm -rf .idea
