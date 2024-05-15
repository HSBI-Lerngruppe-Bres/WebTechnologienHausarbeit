# Web Technologies Project: UNO/Bruno

![Project Logo](bruno/static/images/logo.png)

## Introduction

UNO/Bruno is a web-based game application developed using Flask and SQLAlchemy in Python. The goal of this project is to create an intuitive and user-friendly platform that allows users to play an online version of the popular card game UNO.

## Technology Stack

Programming Language: Python 3
Web Framework: Flask
Database Toolkit: SQLAlchemy
Real-time Communication: Flask-SocketIO
Frontend Technologies: HTML, CSS, JavaScript, Bootstrap
Dependency Management: Poetry

## Installation

Follow these steps to set up the project locally:

1. Clone the repository:
   `git clone https://github.com/HSBI-Lerngruppe-Bres/WebTechnologienHausarbeit`
2. Navigate to the project directory:
   `cd WebTechnologienHausarbeit`
3. Install Poetry if it's not already installed:
   `pipx install poetry`
4. Install dependencies using Poetry:
   `poetry install`
5. Activate the virtual environment:
   `poetry shell`
6. Initialize Database:
   `flask --app bruno:create_app db upgrade`
   `flask --app bruno:create_app populate_cards`
7. Start the server:
   `python run.py`

## Usage

Once the server is running, navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser to access the game. Users can create an account, join a game, and start playing UNO with friends in real-time.

## License

This project is licensed under the MIT License. For more information, see the LICENSE file.
