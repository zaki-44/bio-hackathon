from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for sellers (in production, use a database)
sellers_db = {
    1: {
        "id": 1,
        "name": "John's Organic Farm",
        "email": "john@organicfarm.com",
        "phone": "+1234567890",
        "business_type": "Organic Produce",
        "location": "California, USA",
        "status": "pending",  # pending, accepted, refused
        "created_at": "2024-01-15T10:30:00",
        "description": "Fresh organic vegetables and fruits"
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
        "description": "Agricultural equipment and tools"
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
        "description": "High-quality seeds for various crops"
    }
}

next_seller_id = 4  # Counter for new seller IDs

@app.route("/")
def home():
    return "Hello, Zaki!"

@app.route("/api/test")
def test():
    return jsonify({"message": "Backend is connected!", "status": "success"})

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy", "service": "bio-hackathon-backend"})

# Admin Dashboard Endpoints

@app.route("/api/admin/sellers", methods=["GET"])
def get_all_sellers():
    """Get all sellers with optional status filter"""
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

@app.route("/api/admin/sellers/<int:seller_id>", methods=["GET"])
def get_seller(seller_id):
    """Get a specific seller by ID"""
    seller = sellers_db.get(seller_id)
    
    if not seller:
        return jsonify({
            "success": False,
            "error": "Seller not found"
        }), 404
    
    return jsonify({
        "success": True,
        "seller": seller
    })

@app.route("/api/admin/sellers/<int:seller_id>/accept", methods=["POST"])
def accept_seller(seller_id):
    """Accept a seller application"""
    seller = sellers_db.get(seller_id)
    
    if not seller:
        return jsonify({
            "success": False,
            "error": "Seller not found"
        }), 404
    
    if seller["status"] == "accepted":
        return jsonify({
            "success": False,
            "error": "Seller is already accepted"
        }), 400
    
    # Update seller status
    seller["status"] = "accepted"
    seller["reviewed_at"] = datetime.now().isoformat()
    
    return jsonify({
        "success": True,
        "message": f"Seller '{seller['name']}' has been accepted",
        "seller": seller
    })

@app.route("/api/admin/sellers/<int:seller_id>/refuse", methods=["POST"])
def refuse_seller(seller_id):
    """Refuse/reject a seller application"""
    seller = sellers_db.get(seller_id)
    
    if not seller:
        return jsonify({
            "success": False,
            "error": "Seller not found"
        }), 404
    
    if seller["status"] == "refused":
        return jsonify({
            "success": False,
            "error": "Seller is already refused"
        }), 400
    
    # Get refusal reason from request body (optional)
    data = request.get_json() or {}
    reason = data.get("reason", "No reason provided")
    
    # Update seller status
    seller["status"] = "refused"
    seller["refused_reason"] = reason
    seller["reviewed_at"] = datetime.now().isoformat()
    
    return jsonify({
        "success": True,
        "message": f"Seller '{seller['name']}' has been refused",
        "seller": seller
    })

@app.route("/api/admin/sellers/stats", methods=["GET"])
def get_seller_stats():
    """Get statistics about sellers for admin dashboard"""
    total = len(sellers_db)
    pending = sum(1 for s in sellers_db.values() if s["status"] == "pending")
    accepted = sum(1 for s in sellers_db.values() if s["status"] == "accepted")
    refused = sum(1 for s in sellers_db.values() if s["status"] == "refused")
    
    return jsonify({
        "success": True,
        "stats": {
            "total": total,
            "pending": pending,
            "accepted": accepted,
            "refused": refused
        }
    })

# Optional: Endpoint to add a seller (for testing purposes)
@app.route("/api/admin/sellers", methods=["POST"])
def create_seller():
    """Create a new seller application (for testing)"""
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
        "description": data.get("description", "")
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
