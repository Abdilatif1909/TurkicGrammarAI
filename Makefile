.PHONY: migrate makemigrations superuser test run

migrate:
	cd backend && python manage.py migrate

makemigrations:
	cd backend && python manage.py makemigrations

superuser:
	cd backend && python manage.py createsuperuser

test:
	cd backend && python manage.py test

run:
	cd backend && python manage.py runserver 0.0.0.0:8000
