from app import app, db
from models import User, Product
from datetime import datetime

def seed_products():
    with app.app_context():
        print("Seeding products...")
        
        # Create a farmer user if not exists
        farmer = User.query.filter_by(username="farmer_john").first()
        if not farmer:
            farmer = User(
                username="farmer_john",
                email="john@farm.com",
                user_type="farmer",
                is_active=True
            )
            farmer.set_password("password")
            db.session.add(farmer)
            db.session.commit()
            print("Created farmer_john")
        else:
            print("farmer_john already exists")
            
        # Create products
        products_data = [
            {
                "name": "Organic Tomatoes",
                "description": "Fresh organic tomatoes from the garden",
                "price": 2.50,
                "quantity": 100,
                "unit": "kg",
                "category": "Vegetables",
                "location": "Farm A",
                "is_available": True
            },
            {
                "name": "Fresh Eggs",
                "description": "Free range eggs",
                "price": 5.00,
                "quantity": 50,
                "unit": "dozen",
                "category": "Dairy & Eggs",
                "location": "Farm A",
                "is_available": True
            },
            {
                "name": "Sweet Corn",
                "description": "Sweet and juicy corn",
                "price": 1.00,
                "quantity": 200,
                "unit": "ear",
                "category": "Vegetables",
                "location": "Farm A",
                "is_available": True
            },
            {
                "name": "Potatoes",
                "description": "Russet potatoes, great for baking",
                "price": 1.20,
                "quantity": 500,
                "unit": "kg",
                "category": "Vegetables",
                "location": "Farm A",
                "is_available": True
            },
            {
                "name": "Strawberries",
                "description": "Sweet red strawberries",
                "price": 4.00,
                "quantity": 30,
                "unit": "box",
                "category": "Fruits",
                "location": "Farm A",
                "is_available": True
            }
        ]
        
        count = 0
        for p_data in products_data:
            # Check if product exists for this farmer
            existing = Product.query.filter_by(farmer_id=farmer.id, name=p_data["name"]).first()
            if not existing:
                product = Product(
                    farmer_id=farmer.id,
                    name=p_data["name"],
                    description=p_data["description"],
                    price=p_data["price"],
                    quantity=p_data["quantity"],
                    unit=p_data["unit"],
                    category=p_data["category"],
                    location=p_data["location"],
                    is_available=p_data["is_available"]
                )
                db.session.add(product)
                count += 1
                print(f"Added product: {p_data['name']}")
        
        if count > 0:
            db.session.commit()
            print(f"Successfully added {count} products")
        else:
            print("No new products added")

if __name__ == "__main__":
    seed_products()
