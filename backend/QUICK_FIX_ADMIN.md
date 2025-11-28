# Quick Fix for Admin Login Issue

## Problem

Getting "incorrect username or password" when trying to log in as admin.

## Solution

### Step 1: Run the Fix Script

Open a terminal in the `bio-hackathon/backend` directory and run:

```bash
python fix_admin_login.py
```

This script will:

- Check if admin account exists
- Create one if it doesn't
- Reset password to 'admin123' if needed
- Verify everything works

### Step 2: Alternative - Manual Fix

If the script doesn't work, try this:

```bash
cd bio-hackathon/backend
python reset_admin.py
```

### Step 3: Verify Login

After running the fix, try logging in with:

- **Username**: `admin`
- **Password**: `admin123`
- **User Type**: Leave as "Any type" OR select "Admin"

### Common Issues:

1. **User Type Mismatch**: If you select "Admin" in the dropdown but the account type doesn't match, you'll get an error. Try leaving it as "Any type" first.

2. **Account Doesn't Exist**: The admin account might not exist. Run the fix script above.

3. **Wrong Password**: The password might have been changed. Run the reset script.

4. **Case Sensitivity**: Make sure username is exactly `admin` (lowercase).

### Step 4: Test Directly

You can also test the login via API:

```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

If this works, the issue is in the frontend. If it doesn't, the issue is in the backend/database.

### Step 5: Check Database Directly

If nothing works, check the database:

```bash
cd bio-hackathon/backend
python -c "from app import app; from models import User; app.app_context().push(); u = User.query.filter_by(username='admin').first(); print('Found:', u.username if u else 'None', '| Type:', u.user_type if u else 'N/A')"
```
