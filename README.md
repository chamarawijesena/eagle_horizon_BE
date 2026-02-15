# Eagle Horizon Backend

A Django REST Framework API for the Eagle Horizon project.

## Project Structure

```
eagle_horizon_be/
├── eagle_horizon/          # Project settings and configuration
│   ├── settings.py         # Django settings
│   ├── urls.py             # URL routing
│   ├── wsgi.py             # WSGI application
│   └── __init__.py
├── core/                   # Core application
│   ├── models.py           # Database models
│   ├── views.py            # API views
│   ├── urls.py             # App URL routing
│   └── admin.py            # Admin configuration
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## Prerequisites

- Python 3.9+
- pip (Python package manager)
- Virtual environment (recommended)

## Installation

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file:**
   ```bash
   copy .env.example .env
   ```
   Update the `.env` file with your configuration.

## Running the Project

1. **Apply database migrations:**
   ```bash
   python manage.py migrate
   ```

2. **Create a superuser (admin account):**
   ```bash
   python manage.py createsuperuser
   ```

3. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/`

## API Endpoints

- Health Check: `GET /api/health/`
- Admin Panel: `GET /admin/`

## Environment Variables

Create a `.env` file in the project root based on `.env.example`:

- `SECRET_KEY` - Django secret key (generate a strong one for production)
- `DEBUG` - Set to `False` in production
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `CORS_ALLOWED_ORIGINS` - Comma-separated list of allowed CORS origins

## Development

### Database Migrations

```bash
# Create migrations for changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### Creating a New App

```bash
python manage.py startapp <app_name>
```

Remember to add the app to `INSTALLED_APPS` in `eagle_horizon/settings.py`.

## Testing

```bash
python manage.py test
```

## Deployment

See the Gunicorn configuration in `requirements.txt` for production deployment options.

## License

All rights reserved.

## FE Connection

```bash
Browser
   ↓
React (localhost:3000)
   ↓ HTTP request (fetch / axios)
Django API (localhost:8000)
   ↓
PostgreSQL
```