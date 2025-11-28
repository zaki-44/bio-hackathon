# Backend Structure

This document describes the improved backend structure for better maintainability and organization.

## Directory Structure

```
backend/
├── app.py                 # Main Flask application (simplified)
├── config.py              # Configuration settings
├── models.py              # Database models
├── auth.py                # Authentication decorators
├── utils.py               # Utility functions
├── create_admin.py        # Script to create admin user
├── routes/                # Route handlers organized by domain
│   ├── __init__.py
│   ├── auth.py            # Authentication routes (register, login, logout, profile)
│   ├── products.py        # Product routes (create, search, get photo)
│   ├── admin.py           # Admin routes (farmer applications, stats)
│   └── farmers.py         # Farmer application routes (certification)
├── uploads/               # Uploaded files
│   └── certifications/    # Farmer certification PDFs
└── instance/              # SQLite database
    └── database.db
```

## Key Improvements

### 1. **Separation of Concerns**
- **config.py**: All configuration settings in one place
- **utils.py**: Reusable utility functions
- **routes/**: Routes organized by domain/feature

### 2. **Modular Route Organization**
- **routes/auth.py**: Authentication endpoints
  - `POST /api/register` - User registration
  - `POST /api/login` - User login
  - `GET /api/profile` - Get user profile
  - `POST /api/logout` - Logout
  - `GET /api/session` - Get session info

- **routes/products.py**: Product management
  - `POST /api/products` - Create product (farmer only)
  - `GET /api/products/<id>/photo` - Get product photo
  - `GET /api/products/search?q=<query>` - Search products

- **routes/admin.py**: Admin operations
  - `GET /api/admin/farmers/applications` - List farmer applications
  - `POST /api/admin/farmers/applications/<id>/approve` - Approve application
  - `POST /api/admin/farmers/applications/<id>/deny` - Deny application
  - `GET /api/admin/farmers/applications/stats` - Get statistics
  - `POST /api/admin/create-admin` - Create admin user

- **routes/farmers.py**: Farmer-specific routes
  - `GET /api/farmers/applications/<id>/certification` - Get certification PDF

### 3. **Simplified app.py**
The main `app.py` file is now much smaller (~177 lines vs 1116 lines) and focuses on:
- Application initialization
- Configuration loading
- Blueprint registration
- Database setup and migrations
- Legacy/test endpoints (can be removed later)

### 4. **Better Code Organization**
- Each route file is focused on a single domain
- Easier to find and modify specific functionality
- Better testability
- Clearer separation of concerns

## Configuration

All configuration is centralized in `config.py`:
- Database URI
- JWT settings
- Session settings
- Upload folder settings
- Allowed file extensions
- Valid user types

## Utilities

Common utilities in `utils.py`:
- `allowed_file()` - Check file extension
- `generate_unique_filename()` - Generate unique filenames
- `get_mime_type()` - Get MIME type from filename
- `ensure_directory_exists()` - Create directories if needed

## Migration Notes

The database migration for `certification_filename` column is handled automatically in `app.py` on startup.

## Legacy Endpoints

Some legacy/test endpoints remain in `app.py`:
- `/test` - Test page
- `/api/admin/sellers` - In-memory seller management (for testing)

These can be removed or moved to a separate test routes file if needed.

