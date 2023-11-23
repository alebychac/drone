
# MUSALA SOFT - Drone Project

## Backend Requirements

* [python3](https://www.python.org/downloads/).

## Backend local development

* Start by clone the repo:

git clone https://github.com/alebychac/drone.git

* Install python3:

** select the latest version from: https://www.python.org/downloads/

* open the project folder

* install the project requirements using:

pip install -r requirements.txt

* start the server:

uvicorn drone.app.main:app --reload

* Now you can open your browser and interact with these URLs:

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost/redoc

### Project local tests

To test the project run:

pytest

### Migrations

I didn't cover database migrations