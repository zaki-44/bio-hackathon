"""
Script to create an admin user for the BioMarket application.
Run this script to create your first admin account.

Usage:
    python create_admin.py
    python create_admin.py --username myadmin --email admin@example.com --password mypassword
"""

import sys
import os
import argparse

# Add the current directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User

def create_admin(username='admin', email='admin@biomarket.com', password='admin123'):
    """Create an admin user"""
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.query.filter_by(user_type='admin').first()
        if existing_admin:
            print(f"❌ Admin user already exists: {existing_admin.username}")
            return False
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            print(f"❌ Username '{username}' already exists")
            return False
        
        if User.query.filter_by(email=email).first():
            print(f"❌ Email '{email}' already exists")
            return False
        
        # Create admin user
        admin_user = User(
            username=username,
            email=email,
            user_type='admin'
        )
        admin_user.set_password(password)
        
        db.session.add(admin_user)
        db.session.commit()
        
        print(f"✅ Admin user created successfully!")
        print(f"   Username: {username}")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        print(f"\n⚠️  Please change the password after first login!")
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create an admin user for BioMarket')
    parser.add_argument('--username', default='admin', help='Admin username (default: admin)')
    parser.add_argument('--email', default='admin@biomarket.com', help='Admin email (default: admin@biomarket.com)')
    parser.add_argument('--password', default='admin123', help='Admin password (default: admin123)')
    
    args = parser.parse_args()
    
    try:
        create_admin(args.username, args.email, args.password)
    except Exception as e:
        print(f"❌ Error creating admin: {e}")
        sys.exit(1)

