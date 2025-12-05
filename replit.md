# Django Social Network Application

## Overview
This is a Django-based social network application that allows users to create accounts, login, post updates, and manage their profiles. The application has been configured to run seamlessly in the Replit environment.

## Project Structure
- **socialNetworkApp/** - Main Django project directory
  - **core/** - Main app with user authentication and post management
    - **models.py** - User and Post models
    - **views.py** - Login, signup, profile, and post creation views
    - **forms.py** - Custom signup form
    - **urls.py** - URL routing
  - **socialNetworkApp/** - Project settings
    - **settings.py** - Django configuration
    - **urls.py** - Main URL configuration
  - **Templates/** - HTML templates
  - **Static/** - Static files and media uploads
  - **manage.py** - Django management script

## Features
- User registration and authentication
- User profiles with bio and profile pictures
- Post creation with captions
- Account settings to update profile information
- Pagination on profile page (2 posts per page)

## Technology Stack
- Django 5.0.0
- django-crispy-forms 2.1 with Bootstrap 4
- Pillow 10.1.0 (for image handling)
- python-dotenv 1.0.0 (for environment variables)
- SQLite (database)
- Gunicorn 21.2.0 (for production deployment)

## Environment Variables
The following environment variables are configured:
- `SECRET_KEY` - Django secret key for cryptographic signing
- `DEBUG` - Set to "True" for development mode

## Database
The application uses SQLite as its database. Migrations have been applied and the database is ready to use.

## Running the Application
The application is configured to run on port 5000 using Django's development server:
```bash
cd socialNetworkApp && python manage.py runserver 0.0.0.0:5000
```

## Deployment
The application is configured for Autoscale deployment using Gunicorn as the WSGI server. The deployment will automatically scale based on traffic.

## Replit-Specific Configuration
The following changes were made to ensure compatibility with Replit:
1. **ALLOWED_HOSTS** - Set to `['*']` to allow access from Replit's proxy
2. **X_FRAME_OPTIONS** - Set to `'ALLOWALL'` to allow embedding in Replit's iframe
3. **CSRF_TRUSTED_ORIGINS** - Configured for Replit domains
4. **Server binding** - Development server binds to `0.0.0.0:5000`

## Recent Changes
- December 5, 2025: Initial Replit environment setup
  - Installed Python 3.11 and all dependencies
  - Configured environment variables
  - Updated Django settings for Replit compatibility
  - Ran database migrations
  - Configured workflow and deployment settings
  - Created project documentation

## User Preferences
None specified yet.

## Project Architecture
This is a standard Django application following the MVT (Model-View-Template) pattern:
- Models define User and Post data structures
- Views handle request/response logic for authentication and CRUD operations
- Templates render the HTML pages
- Static files include CSS, JavaScript, and user-uploaded media
