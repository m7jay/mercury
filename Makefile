.PHONY: static
static:
	tailwindcss -i ./static/src/main.css -o ./static/src/output.css --minify

.PHONY: mercury
mercury:
	make static
	python manage.py migrate
	python manage.py runserver