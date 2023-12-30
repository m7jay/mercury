.PHONY: static
static:
	tailwindcss -i ./static/src/main.css -o ./static/src/output.css --minify --watch

.PHONY: mercury
mercury:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver

.PHONY: shell
shell:
	python manage.py migrate
	python manage.py shell_plus --ipython
