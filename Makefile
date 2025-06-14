.PHONY: static
static:
	tailwindcss -i ./static/src/main.css -o ./static/src/output.css --minify --watch

.PHONY: stop
stop:
	docker compose -f ./docker-compose.local.yml ps
	echo "stopping.."
	docker compose -f ./docker-compose.local.yml stop

.PHONY: mercury
mercury:
	docker compose -f ./docker-compose.local.yml up -d
	docker compose -f ./docker-compose.local.yml ps

.PHONY: shell
shell:
	docker compose -f ./docker-compose.local.yml run --rm mercury-service python manage.py shell_plus --ipython

.PHONY: migrate
migrate:
	docker compose -f ./docker-compose.local.yml run --rm mercury-service python manage.py migrate

.PHONY: makemigrations
makemigrations:
	docker compose -f ./docker-compose.local.yml run --rm mercury-service python manage.py makemigrations

.PHONY: build
build:
	docker compose -f ./docker-compose.build.yml build mercury-service

.PHONY: build-no-cache
build-no-cache:
	docker compose -f ./docker-compose.build.yml build --no-cache mercury-service

.PHONY: delpoy-check
deploy-check:
	docker compose -f ./docker-compose.local.yml run --rm mercury-service python manage.py check --deploy

.PHONY: deploy
deploy:
	git pull
	make build
	make migrate
	make deploy-check
	make mercury


