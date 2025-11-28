"""Main Flask application"""
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from config import Config
from utils import ensure_directory_exists
import os
from sqlalchemy import inspect, text

# Import blueprints
from routes.auth import auth_bp
from routes.products import products_bp
from routes.admin import admin_bp
from routes.farmers import farmers_bp

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Load configuration
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Configure JWT to handle dictionary identities
@jwt.user_identity_loader
def user_identity_lookup(user):
    """Convert user dict to JSON-serializable format"""
    if isinstance(user, dict):
        return user
    return str(user)

# Create uploads directory if it doesn't exist
ensure_directory_exists(Config.UPLOAD_FOLDER)
ensure_directory_exists(os.path.join(Config.UPLOAD_FOLDER, 'certifications'))

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(farmers_bp)

# Database initialization and migration
with app.app_context():
    db.create_all()
    
    # Add certification_filename column if it doesn't exist (migration)
    try:
        inspector = inspect(db.engine)
        
        # Check if farmer_applications table exists
        if 'farmer_applications' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('farmer_applications')]
            
            if 'certification_filename' not in columns:
                with db.engine.begin() as conn:
                    conn.execute(text('ALTER TABLE farmer_applications ADD COLUMN certification_filename VARCHAR(255)'))
                print("✓ Added certification_filename column to farmer_applications table")
    except Exception as e:
        print(f"Migration note: {e}")

# Legacy/test routes (can be removed later if not needed)
@app.route("/test")
def test_page():
    """Serve the test page from Flask"""
    return send_from_directory('.', 'test_all_routes.html')

# Legacy sellers endpoints (in-memory, for testing)
sellers_db = {
    1: {
        "id": 1,
        "name": "John's Organic Farm",
        "email": "john@organicfarm.com",
        "phone": "+1234567890",
        "business_type": "Organic Produce",
        "location": "California, USA",
        "status": "pending",
        "created_at": "2024-01-15T10:30:00",
        "description": "Fresh organic vegetables and fruits",
        "rating": 0.0
    },
    2: {
        "id": 2,
        "name": "Green Valley Supplies",
        "email": "contact@greenvalley.com",
        "phone": "+1987654321",
        "business_type": "Farming Equipment",
        "location": "Texas, USA",
        "status": "pending",
        "created_at": "2024-01-16T14:20:00",
        "description": "Agricultural equipment and tools",
        "rating": 0.0
    },
    3: {
        "id": 3,
        "name": "BioTech Seeds Co.",
        "email": "info@biotechseeds.com",
        "phone": "+1555666777",
        "business_type": "Seed Supplier",
        "location": "Iowa, USA",
        "status": "pending",
        "created_at": "2024-01-17T09:15:00",
        "description": "High-quality organic seeds",
        "rating": 0.0
    }
}

next_seller_id = 4

@app.route("/api/admin/sellers", methods=["GET"])
def get_all_sellers():
    """Get all sellers with optional status filter (legacy/test endpoint)"""
    from flask import request
    from datetime import datetime
    
    status_filter = request.args.get("status", None)
    
    sellers = list(sellers_db.values())
    
    if status_filter:
        sellers = [s for s in sellers if s["status"] == status_filter]
    
    # Sort by created_at (newest first)
    sellers.sort(key=lambda x: x["created_at"], reverse=True)
    
    return jsonify({
        "success": True,
        "count": len(sellers),
        "sellers": sellers
    })

@app.route("/api/admin/sellers", methods=["POST"])
def create_seller():
    """Create a new seller application (legacy/test endpoint)"""
    from flask import request
    from datetime import datetime
    global next_seller_id
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ["name", "email", "business_type"]
    for field in required_fields:
        if field not in data:
            return jsonify({
                "success": False,
                "error": f"Missing required field: {field}"
            }), 400
    
    # Create new seller
    new_seller = {
        "id": next_seller_id,
        "name": data["name"],
        "email": data["email"],
        "phone": data.get("phone", ""),
        "business_type": data["business_type"],
        "location": data.get("location", ""),
        "status": "pending",
        "created_at": datetime.now().isoformat(),
        "description": data.get("description", ""),
        "rating": float(data.get("rating", 0.0))
    }
    
    sellers_db[next_seller_id] = new_seller
    next_seller_id += 1
    
    return jsonify({
        "success": True,
        "message": "Seller application created",
        "seller": new_seller
    }), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000)
