"""Reset or create admin account - removes existing admin and creates new one"""
from app import app, db
from models import User

with app.app_context():
    print("Resetting admin account...")
    
    # Delete existing admin if any
    existing_admin = User.query.filter_by(user_type='admin').first()
    if existing_admin:
        print(f"Removing existing admin: {existing_admin.username}")
        db.session.delete(existing_admin)
        db.session.commit()
    
    # Also check if username 'admin' exists with different type
    admin_username = User.query.filter_by(username='admin').first()
    if admin_username and admin_username.user_type != 'admin':
        print(f"Removing user with username 'admin' (type: {admin_username.user_type})")
        db.session.delete(admin_username)
        db.session.commit()
    
    # Create new admin
    admin_user = User(
        username='admin',
        email='admin@biomarket.com',
        user_type='admin'
    )
    admin_user.set_password('admin123')
    
    db.session.add(admin_user)
    db.session.commit()
    
    # Verify
    test_user = User.query.filter_by(username='admin').first()
    if test_user and test_user.check_password('admin123'):
        print("✅ Admin account created and verified!")
        print(f"   Username: {test_user.username}")
        print(f"   Email: {test_user.email}")
        print(f"   Type: {test_user.user_type}")
        print(f"   Password: admin123")
        print("\nYou can now login with:")
        print("   Username: admin")
        print("   Password: admin123")
    else:
        print("❌ Failed to create admin account")

