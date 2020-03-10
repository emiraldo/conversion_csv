migrate:
	docker-compose run --rm django ./manage.py makemigrations 
	docker-compose run --rm django ./manage.py migrate
requirements:
	docker-compose run --rm django pip install -r requirements.txt
statics:
	docker-compose run --rm django ./manage.py collectstatic --no-input 
superuser:
	docker-compose run --rm django ./manage.py createsuperuser
app:
	docker-compose run --rm django ./manage.py startapp $(APP_NAME)
clean:
	rm -rf src/*/migrations/00**.py
	find . -name "*.pyc" -exec rm -- {} +
	rm -rf src/*/migrations/__pycache__/*
reset:
	docker-compose down -v
	rm -rf .pgdata/
