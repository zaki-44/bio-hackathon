from app import app
from models import Product

def verify_products():
    with app.app_context():
        count = Product.query.count()
        print(f"Total products in DB: {count}")
        
        products = Product.query.all()
        for p in products:
            print(f"- {p.name} (${p.price})")

if __name__ == "__main__":
    verify_products()
