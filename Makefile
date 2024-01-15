ARG := $(wordlist 2, $(words $(MAKECMDGOALS)), $(MAKECMDGOALS))
$(eval $(ARG):;@true)

perms:
	sudo chown -hR ${USER}:${USER} .

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

enter:
	docker-compose exec $(ARG) bash

setup_install:
	bash scripts/setup-install.sh

setup_venv:
	bash scripts/setup-venv.sh

test:
	docker-compose run web pytest 
