install:
	pip install uv
	pip install gunicorn uvicorn
	uv venv
	uv pip install -r requirements.txt

dev:
	python manage.py runserver

lint:
	flake8 .

start:
	python manage.py runserver

render-start:
	gunicorn task_manager.wsgi

build:
	./build.sh

tests:
	python manage.py test

migrate:
	python manage.py migrate
