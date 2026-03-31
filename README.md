# DeFlock SD OSM Processing Backend

## Overview
This backend is a Flask application for processing OpenStreetMap (OSM) data in the DeFlock SD workflow. It includes user authentication, database initialization, and web endpoints for interacting with processed tile data.

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
- `nginx_flask_8587.conf` is an example Nginx configuration for production reverse proxy.
- Use `docker-compose.yml` for containerized local development.
