# Eagle Horizon Backend - Copilot Instructions

This is a Django REST Framework project for the Eagle Horizon backend.

## Project Setup Status

- [x] Django project structure created
- [x] Core app initialized with health check endpoint
- [x] Environment configuration with python-decouple
- [x] CORS and REST Framework configured
- [x] Requirements.txt with essential dependencies
- [ ] Virtual environment setup (user needs to run)
- [ ] Dependencies installation (user needs to run)
- [ ] Database migrations (user needs to run)

## Quick Start

1. Create and activate virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and update as needed
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Start server: `python manage.py runserver`

## Development Guidelines

- Add new apps to `INSTALLED_APPS` in settings.py
- Use the `TimeStampedModel` abstract base class for models with timestamps
- API endpoints should follow REST conventions
- Configure CORS origins in `.env` file

## Available Endpoints

- `/api/health/` - Health check endpoint
- `/admin/` - Django admin panel
