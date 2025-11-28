"""
Fix admin login issues - checks and creates admin account
Run this script to ensure admin account exists and works
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User

def main():
    with app.app_context():
        print("\n" + "="*60)
        print("ADMIN ACCOUNT DIAGNOSTIC & FIX")
        print("="*60 + "\n")
        
        # Step 1: Check all users
        all_users = User.query.all()
        print(f"Step 1: Found {len(all_users)} total user(s) in database")
        
        if all_users:
            print("\nAll users:")
            for u in all_users:
                print(f"  - Username: '{u.username}' | Type: '{u.user_type}' | Email: '{u.email}'")
        
        # Step 2: Check for admin
        admin = User.query.filter_by(user_type='admin').first()
        admin_by_username = User.query.filter_by(username='admin').first()
        
        print(f"\nStep 2: Checking for admin account...")
        if admin:
            print(f"  ✅ Found admin account: {admin.username}")
            print(f"     Email: {admin.email}")
            print(f"     Active: {admin.is_active}")
            
            # Test password
            test_passwords = ['admin123', 'admin', 'password']
            password_works = False
            for pwd in test_passwords:
                if admin.check_password(pwd):
                    print(f"  ✅ Password '{pwd}' works!")
                    password_works = True
                    break
            
            if not password_works:
                print(f"  ❌ None of the test passwords work")
                print(f"  Resetting password to 'admin123'...")
                admin.set_password('admin123')
                db.session.commit()
                print(f"  ✅ Password reset to 'admin123'")
        else:
            print(f"  ❌ No admin account found")
            
            # Check if username 'admin' exists with different type
            if admin_by_username and admin_by_username.user_type != 'admin':
                print(f"  ⚠️  Username 'admin' exists but type is '{admin_by_username.user_type}'")
                print(f"  Converting to admin...")
                admin_by_username.user_type = 'admin'
                admin_by_username.set_password('admin123')
                db.session.commit()
                print(f"  ✅ Converted to admin account")
            else:
                print(f"  Creating new admin account...")
                new_admin = User(
                    username='admin',
                    email='admin@biomarket.com',
                    user_type='admin'
                )
                new_admin.set_password('admin123')
                db.session.add(new_admin)
                db.session.commit()
                print(f"  ✅ Admin account created!")
        
        # Step 3: Final verification
        print(f"\nStep 3: Final verification...")
        final_admin = User.query.filter_by(username='admin', user_type='admin').first()
        if final_admin:
            if final_admin.check_password('admin123'):
                print(f"  ✅ Admin account verified and ready!")
                print(f"\n" + "="*60)
                print("LOGIN CREDENTIALS:")
                print("="*60)
                print(f"  Username: admin")
                print(f"  Password: admin123")
                print(f"  User Type: admin (select 'Admin' in dropdown)")
                print("="*60 + "\n")
            else:
                print(f"  ❌ Password verification failed - something is wrong")
        else:
            print(f"  ❌ Admin account not found after creation - check database")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

