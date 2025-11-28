"""Script to check and create admin account"""
from app import app, db
from models import User

with app.app_context():
    print("=" * 50)
    print("Checking for admin accounts...")
    print("=" * 50)
    
    # Check all users
    all_users = User.query.all()
    print(f"\nTotal users in database: {len(all_users)}")
    
    if all_users:
        print("\nAll users:")
        for user in all_users:
            print(f"  - ID: {user.id}")
            print(f"    Username: {user.username}")
            print(f"    Email: {user.email}")
            print(f"    Type: {user.user_type}")
            print(f"    Active: {user.is_active}")
            print()
    
    # Check specifically for admin
    admin = User.query.filter_by(user_type='admin').first()
    
    if admin:
        print(f"✅ Admin account found!")
        print(f"   Username: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Type: {admin.user_type}")
        
        # Test password
        test_password = "admin123"
        if admin.check_password(test_password):
            print(f"   ✅ Password 'admin123' is correct")
        else:
            print(f"   ❌ Password 'admin123' is incorrect")
            print(f"   Try other common passwords or reset it")
    else:
        print("\n❌ No admin account found!")
        print("\nCreating admin account...")
        
        # Create admin
        admin_user = User(
            username='admin',
            email='admin@biomarket.com',
            user_type='admin'
        )
        admin_user.set_password('admin123')
        
        db.session.add(admin_user)
        db.session.commit()
        
        print("✅ Admin account created successfully!")
        print(f"   Username: admin")
        print(f"   Email: admin@biomarket.com")
        print(f"   Password: admin123")
    
    print("\n" + "=" * 50)

