.PHONY: static
static:
	tailwindcss -i ./static/src/main.css -o ./static/src/output.css --minify
	python manage.py makemigrations

.PHONY: mercury
mercury:
	make static
	python manage.py migrate
	python manage.py runserver

.PHONY: shell
shell:
	make static
	python manage.py migrate
	python manage.py shell_plus --ipython
