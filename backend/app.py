from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from datetime import timedelta
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Create database tables
with app.app_context():
    db.create_all()

# Valid user types
VALID_USER_TYPES = ['farmer', 'transporter', 'user']

@app.route("/")
def home():
    return "Hello, Zaki!"

@app.route("/api/test")
def test():
    return jsonify({"message": "Backend is connected!", "status": "success"})

@app.route("/api/health")
def health():
    return jsonify({"status": "healthy", "service": "bio-hackathon-backend"})

@app.route("/api/register", methods=["POST"])
def register():
    """Register a new user (farmer, transporter, or user)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        user_type = data.get("user_type", "").lower()
        
        # Validate fields
        if not username or not email or not password:
            return jsonify({
                "error": "Missing required fields",
                "message": "Username, email, and password are required"
            }), 400
        
        if user_type not in VALID_USER_TYPES:
            return jsonify({
                "error": "Invalid user type",
                "message": f"User type must be one of: {', '.join(VALID_USER_TYPES)}"
            }), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({
                "error": "Username already exists",
                "message": "Please choose a different username"
            }), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({
                "error": "Email already exists",
                "message": "This email is already registered"
            }), 400
        
        # Create new user
        new_user = User(
            username=username,
            email=email,
            user_type=user_type
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate access token
        access_token = create_access_token(
            identity={
                'id': new_user.id,
                'username': new_user.username,
                'user_type': new_user.user_type
            }
        )
        
        return jsonify({
            "message": "User registered successfully",
            "user": new_user.to_dict(),
            "access_token": access_token
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Registration failed",
            "message": str(e)
        }), 500

@app.route("/api/login", methods=["POST"])
def login():
    """Login endpoint for farmer, transporter, and user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        username = data.get("username")
        password = data.get("password")
        user_type = data.get("user_type", "").lower()  # Optional: filter by user type
        
        if not username or not password:
            return jsonify({
                "error": "Missing credentials",
                "message": "Username and password are required"
            }), 400
        
        # Find user by username
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({
                "error": "Invalid credentials",
                "message": "Username or password is incorrect"
            }), 401
        
        # Check password
        if not user.check_password(password):
            return jsonify({
                "error": "Invalid credentials",
                "message": "Username or password is incorrect"
            }), 401
        
        # Optional: verify user type matches if provided
        if user_type and user.user_type != user_type:
            return jsonify({
                "error": "User type mismatch",
                "message": f"User is registered as {user.user_type}, not {user_type}"
            }), 403
        
        # Check if user is active
        if not user.is_active:
            return jsonify({
                "error": "Account disabled",
                "message": "Your account has been disabled. Please contact support."
            }), 403
        
        # Generate access token
        access_token = create_access_token(
            identity={
                'id': user.id,
                'username': user.username,
                'user_type': user.user_type
            }
        )
        
        return jsonify({
            "message": "Login successful",
            "user": user.to_dict(),
            "access_token": access_token
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Login failed",
            "message": str(e)
        }), 500

@app.route("/api/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """Get current user's profile"""
    try:
        current_user = get_jwt_identity()
        user_id = current_user.get('id')
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                "error": "User not found"
            }), 404
        
        return jsonify({
            "user": user.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Failed to fetch profile",
            "message": str(e)
        }), 500

@app.route("/api/verify-token", methods=["GET"])
@jwt_required()
def verify_token():
    """Verify if the current token is valid"""
    try:
        current_user = get_jwt_identity()
        return jsonify({
            "valid": True,
            "user": current_user
        }), 200
    except Exception as e:
        return jsonify({
            "valid": False,
            "error": str(e)
        }), 401

if __name__ == "__main__":
    app.run(debug=True, port=5000)
