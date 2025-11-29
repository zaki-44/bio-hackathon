from app import app, db
from models import User, Package
from datetime import datetime

def seed_delivery():
    with app.app_context():
        print("Seeding delivery data...")
        
        # Create transporter
        transporter = User.query.filter_by(username="transporter1").first()
        if not transporter:
            transporter = User(
                username="transporter1",
                email="transporter1@test.com",
                user_type="transporter"
            )
            transporter.set_password("password")
            db.session.add(transporter)
            db.session.commit()
            print("Created transporter1")
        else:
            print("transporter1 already exists")
            
        # Create packages
        packages = [
            {
                "recipient_name": "Alice Smith",
                "recipient_address": "123 Main St, Cityville",
                "tracking_number": "TRK001",
                "status": "pending"
            },
            {
                "recipient_name": "Bob Jones",
                "recipient_address": "456 Oak Ave, Townburg",
                "tracking_number": "TRK002",
                "status": "in_transit"
            },
            {
                "recipient_name": "Charlie Brown",
                "recipient_address": "789 Pine Ln, Villageton",
                "tracking_number": "TRK003",
                "status": "delivered"
            }
        ]
        
        for pkg_data in packages:
            existing = Package.query.filter_by(tracking_number=pkg_data["tracking_number"]).first()
            if not existing:
                pkg = Package(
                    transporter_id=transporter.id,
                    recipient_name=pkg_data["recipient_name"],
                    recipient_address=pkg_data["recipient_address"],
                    tracking_number=pkg_data["tracking_number"],
                    status=pkg_data["status"]
                )
                db.session.add(pkg)
                print(f"Created package {pkg_data['tracking_number']}")
        
        db.session.commit()
        print("Seeding complete!")

if __name__ == "__main__":
    seed_delivery()
