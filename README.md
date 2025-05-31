# Django Sample Project

This is a sample Django project using Poetry for dependency management.

## Prerequisites

- Python 3.9 or higher
- Poetry

## Setup

1. Install dependencies:
```bash
poetry install
```

2. Activate the virtual environment:
```bash
poetry shell
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## Development

- Format code:
```bash
poetry run black .
```

- Run tests:
```bash
poetry run pytest
```

## Project Structure

- `configuration/` - Main Django project directory
- `core/` - Core application directory
- `manage.py` - Django's command-line utility 