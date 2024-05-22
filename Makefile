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

rrdb:
	rm instance/app.db
	flask --app bruno db upgrade
	flask --app bruno populate_cards
	python run.py

rcdb:
	flask --app bruno db upgrade
	flask --app bruno populate_cards
	python run.py