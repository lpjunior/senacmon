PY=python
MANAGE=$(PY) src/manage.py

.PHONY: migrate seed seed-extras reset reset-user demo

migrate:
	$(MANAGE) makemigrations
	$(MANAGE) migrate

seed:
	$(MANAGE) seed_senacmon

seed-extras:
	$(MANAGE) seed_extras_senacmon

reset:
	$(MANAGE) reset_senacmon --confirm

reset-user:
	# uso: make reset-user USER=luis
	$(MANAGE) reset_senacmon --user $(USER) --confirm

demo:
	$(MAKE) reset
	$(MAKE) seed
	$(MAKE) seed-extras
