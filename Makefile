# Makefile for managing a Flask application

# Variables
FLASK_APP = bruno
DB_URI = sqlite:///app.db

.PHONY: setup run init-db migrate upgrade

setup:
	@echo "Setting up the environment variables..."
	export FLASK_APP=$(FLASK_APP)
	export SQLALCHEMY_DATABASE_URI=$(DB_URI)
	@echo "Environment variables set!"

run:
	@echo "Running the Flask application..."
	flask run

init-db:
	@echo "Initializing the database..."
	flask db init

migrate:
	@echo "Creating migration files..."
	flask db migrate

upgrade:
	@echo "Applying database migrations..."
	flask db upgrade

downgrade:
	@echo "Reverting the last database migration..."
	flask db downgrade
