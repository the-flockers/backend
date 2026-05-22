# DeFlock SD OSM Processing Backend

## Overview
This backend intends to provide interfacing for navigation and ALPR location data via OSM data. Data is passed through the API into internal [OpenRouteService](https://openrouteservice.org/) instance which provides navigational data.

## Prerequisites
- Python 3.8+
- pip
- virtualenv (recommended)

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
```bash
# Initialize the db
flask --app flaskr init-db

# Run the development server
flask --app flaskr run
```

## Structure
- `flaskr/` - application package
  - `__init__.py` - app factory and configuration
  - `auth.py` - authentication routes and helpers
  - `db.py` - SQLite DB connections and migrations
  - `schema.sql` - database schema definition
  - `templates/` - Jinja2 templates
- `instance/` - instance folder with SQLite DB

## Notes
- Use `docker-compose.yml` for containerized development/deployment.
