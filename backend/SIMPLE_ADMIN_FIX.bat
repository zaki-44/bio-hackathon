@echo off
echo ========================================
echo Admin Account Fix Script
echo ========================================
echo.

cd /d %~dp0

echo Running fix script...
python fix_admin_login.py

echo.
echo ========================================
echo If you see errors above, try:
echo   1. Make sure Flask backend is not running
echo   2. Check that database file exists
echo   3. Try: python reset_admin.py
echo ========================================
pause

