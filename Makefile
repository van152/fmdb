.PHONY: test cached verify-v11 lint config

test:
	py -V:3.12 -B scripts/t145_final_regression.py --selftest

cached:
	py -V:3.12 -B scripts/t145_final_regression.py --cached

verify-v11:
	py -V:3.12 -B scripts/t77_schema_v11.py --verify

lint:
	py -V:3.12 -B scripts/check_repo.py

config:
	py -V:3.12 -B scripts/fm24_config.py
