# Admin Account Guide

This guide explains how to create and use an admin account in the BioMarket application.

## Creating an Admin Account

There are **two ways** to create an admin account:

### Method 1: Using the Python Script (Recommended)

1. Open a terminal/command prompt
2. Navigate to the backend directory:

   ```bash
   cd bio-hackathon/backend
   ```

3. Run the create_admin script:

   ```bash
   python create_admin.py
   ```

   This will create an admin with default credentials:

   - **Username**: `admin`
   - **Email**: `admin@biomarket.com`
   - **Password**: `admin123`

4. To create a custom admin account:
   ```bash
   python create_admin.py --username myadmin --email admin@example.com --password mypassword
   ```

### Method 2: Using the API Endpoint

You can also create an admin via the API (only works if no admin exists yet):

```bash
curl -X POST http://localhost:5000/api/admin/create-admin \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@biomarket.com",
    "password": "admin123"
  }'
```

Or using a tool like Postman or the browser console.

## Logging In as Admin

1. Go to the login page: `http://localhost:3000/login` (or your frontend URL)

2. Enter your admin credentials:

   - **Username**: `admin` (or your custom username)
   - **Password**: `admin123` (or your custom password)
   - **User Type**: Select "Admin" from the dropdown (optional, but recommended)

3. Click "Login"

4. After successful login, you'll be redirected to the home page. Navigate to the Admin Dashboard.

## Admin Dashboard Features

Once logged in as admin, you can:

### 1. Manage Farmer Applications

- View all farmer registration applications
- See application status (pending, approved, denied)
- View farmer certifications (PDF files)
- **Approve** farmer applications (creates user account for farmer)
- **Deny** farmer applications (with optional reason)

### 2. View Statistics

- Total applications
- Pending applications
- Approved applications
- Denied applications

### 3. Access Admin Routes

All admin routes require authentication and admin privileges:

- `GET /api/admin/farmers/applications` - List all applications
- `POST /api/admin/farmers/applications/<id>/approve` - Approve application
- `POST /api/admin/farmers/applications/<id>/deny` - Deny application
- `GET /api/admin/farmers/applications/stats` - Get statistics
- `GET /api/farmers/applications/<id>/certification` - View certification PDF

## Important Notes

⚠️ **Security Reminders:**

- Change the default password after first login
- Only one admin account can exist in the system (by design)
- Admin accounts cannot be created through regular registration
- Admin routes are protected and require JWT authentication

## Troubleshooting

### "Admin already exists" Error

If you see this error, an admin account already exists. You can:

- Use the existing admin credentials
- Or check the database to find the admin username

### "Authentication required" Error

Make sure you're logged in and your session/token is valid. Try logging out and logging back in.

### Can't Access Admin Dashboard

- Ensure you selected "Admin" as user type during login
- Check that your user_type in the database is 'admin'
- Verify your JWT token includes admin privileges

## Default Admin Credentials

If you used the default script:

- **Username**: `admin`
- **Password**: `admin123`
- **Email**: `admin@biomarket.com`

**⚠️ Change these credentials in production!**
