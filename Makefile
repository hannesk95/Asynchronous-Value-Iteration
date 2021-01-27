all:
	@echo "This is a dummy to prevent running make without explicit target!"

clean: remove_pycharm
	$(MAKE) -C backend/ clean
	$(MAKE) -C cpp_backend/ clean
	$(MAKE) -C tests/ clean
	rm -rf .pytest_cache 

compile:
	$(MAKE) -C cpp_backend/ compile

test:
	python3 -m pytest tests/

remove_interface:
	$(MAKE) -C backend/ remove_interface

remove_pycharm:
	rm -rf .idea
