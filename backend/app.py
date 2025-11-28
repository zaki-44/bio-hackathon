from flask import Flask, jsonify, request, session, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Product
from auth import user_type_required
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
from uuid import uuid4

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS with credentials for sessions


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
        "description": "Fresh organic vegetables and fruits",
        "rating": 0.0  # Rating from 0.0 to 5.0
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
        "rating": 0.0  # Rating from 0.0 to 5.0
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
        "description": "High-quality seeds for various crops",
        "rating": 0.0  # Rating from 0.0 to 5.0
    }
}

next_seller_id = 4  # Counter for new seller IDs

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-for-sessions-change-in-production')
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Changed to Lax for better compatibility
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_PATH'] = '/'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

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
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Create database tables
with app.app_context():
    db.create_all()

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Valid user types
VALID_USER_TYPES = ['farmer', 'transporter', 'user']




@app.route("/test")
def test_page():
    """Serve the test page from Flask"""
    return send_from_directory('.', 'test_all_routes.html')






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





# @app.route("/api/admin/sellers/<int:seller_id>/refuse", methods=["POST"])
# def refuse_seller(seller_id):
#     """Refuse/reject a seller application"""
#     seller = sellers_db.get(seller_id)
    
#     if not seller:
#         return jsonify({
#             "success": False,
#             "error": "Seller not found"
#         }), 404
    
#     if seller["status"] == "refused":
#         return jsonify({
#             "success": False,
#             "error": "Seller is already refused"
#         }), 400
    
#     # Get refusal reason from request body (optional)
#     data = request.get_json() or {}
#     reason = data.get("reason", "No reason provided")
    
#     # Update seller status
#     seller["status"] = "refused"
#     seller["refused_reason"] = reason
#     seller["reviewed_at"] = datetime.now().isoformat()
    
#     return jsonify({
#         "success": True,
#         "message": f"Seller '{seller['name']}' has been refused",
#         "seller": seller
#     })

x
    
    sellers_db[next_seller_id] = new_seller
    next_seller_id += 1
    
    return jsonify({
        "success": True,
        "message": "Seller application created",
        "seller": new_seller
    }), 201
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
        "description": data.get("description", ""),
        "rating": float(data.get("rating", 0.0))  # Rating from 0.0 to 5.0, default 0.0
    }
    
    sellers_db[next_seller_id] = new_seller
    next_seller_id += 1
    
    return jsonify({
        "success": True,
        "message": "Seller application created",
        "seller": new_seller
    }), 201

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
        
        # Store user info in session
        session['user_id'] = new_user.id
        session['username'] = new_user.username
        session['user_type'] = new_user.user_type
        session['logged_in'] = True
        
        # Generate access token (identity must be a string, use additional_claims for user info)
        access_token = create_access_token(
            identity=str(new_user.id),
            additional_claims={
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
        
        # Store user info in session
        session['user_id'] = user.id
        session['username'] = user.username
        session['user_type'] = user.user_type
        session['logged_in'] = True
        
        # Generate access token (identity must be a string, use additional_claims for user info)
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
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
def get_profile():
    """Get current user's profile (session-based)"""
    try:
        # Check if user is logged in via session
        if not session.get('logged_in'):
            return jsonify({
                "error": "Not authenticated",
                "message": "Please login first"
            }), 401
        
        # Get user ID from session
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({
                "error": "Invalid session",
                "message": "User ID not found in session"
            }), 401
        
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

# @app.route("/api/verify-token", methods=["GET"])
# @jwt_required()
# def verify_token():
#     """Verify if the current token is valid"""
#     try:
#         user_id = get_jwt_identity()
#         claims = get_jwt()
        
#         return jsonify({
#             "valid": True,
#             "user_id": user_id,
#             "username": claims.get('username'),
#             "user_type": claims.get('user_type')
#         }), 200
#     except Exception as e:
#         return jsonify({
#             "valid": False,
#             "error": str(e)
#         }), 401

@app.route("/api/logout", methods=["POST"])
def logout():
    """Logout and clear session"""
    try:
        session.clear()
        return jsonify({
            "message": "Logged out successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Logout failed",
            "message": str(e)
        }), 500

@app.route("/api/session", methods=["GET"])
def get_session():
    """Get current session info"""
    logged_in = session.get('logged_in', False)
    return jsonify({
        "logged_in": logged_in,
        "user_id": session.get('user_id'),
        "username": session.get('username'),
        "user_type": session.get('user_type'),
        "session_keys": list(session.keys()),
        "debug": {
            "has_session": bool(session),
            "session_id": session.get('_id', 'no_id')
        }
    }), 200

@app.route("/api/farmers/apply", methods=["POST"])
def submit_farmer_application():
    """Submit a farmer application"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        farm_name = data.get("farm_name")
        location = data.get("location")
        
        # Validate required fields
        if not username or not email or not password or not farm_name or not location:
            return jsonify({
                "error": "Missing required fields",
                "message": "Username, email, password, farm_name, and location are required"
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
        
        # Check if application already exists
        existing_application = FarmerApplication.query.filter(
            (FarmerApplication.username == username) | (FarmerApplication.email == email)
        ).first()
        
        if existing_application:
            if existing_application.status == 'pending':
                return jsonify({
                    "error": "Application already pending",
                    "message": "You already have a pending application. Please wait for admin review."
                }), 400
            elif existing_application.status == 'approved':
                return jsonify({
                    "error": "Application already approved",
                    "message": "Your application has already been approved. Please login instead."
                }), 400
        
        # Create new farmer application
        new_application = FarmerApplication(
            username=username,
            email=email,
            farm_name=farm_name,
            location=location,
            phone=data.get("phone", ""),
            description=data.get("description", ""),
            status="pending"
        )
        new_application.set_password(password)
        
        db.session.add(new_application)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Farmer application submitted successfully. Please wait for admin approval.",
            "application": new_application.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Failed to submit application",
            "message": str(e)
        }), 500


@app.route("/api/admin/farmers/applications", methods=["GET"])
def get_farmer_applications():
    """Get all farmer applications with optional status filter"""
    try:
        status_filter = request.args.get("status", None)
        
        query = FarmerApplication.query
        
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        # Sort by created_at (newest first)
        applications = query.order_by(FarmerApplication.created_at.desc()).all()
        
        return jsonify({
            "success": True,
            "count": len(applications),
            "applications": [app.to_dict() for app in applications]
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Failed to fetch applications",
            "message": str(e)
        }), 500


        @app.route("/api/admin/farmers/applications/<int:application_id>/approve", methods=["POST"])
def approve_farmer_application(application_id):
    """Approve a farmer application and create the user account"""
    try:
        application = FarmerApplication.query.get(application_id)
        
        if not application:
            return jsonify({
                "success": False,
                "error": "Application not found"
            }), 404
        
        if application.status == "approved":
            return jsonify({
                "success": False,
                "error": "Application is already approved"
            }), 400
        
        if application.status == "denied":
            return jsonify({
                "success": False,
                "error": "Cannot approve a denied application"
            }), 400
        
        # Check if user already exists (in case of race condition)
        existing_user = User.query.filter_by(username=application.username).first()
        if existing_user:
            # Update application status but don't create duplicate user
            application.status = "approved"
            application.reviewed_at = datetime.now()
            # Get admin user ID from session or token if available
            try:
                current_user = get_jwt_identity()
                if isinstance(current_user, dict):
                    application.reviewed_by = current_user.get('id')
            except:
                pass  # If no JWT token, leave reviewed_by as None
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": f"Application approved (user already exists)",
                "application": application.to_dict(),
                "user": existing_user.to_dict()
            }), 200
        
        # Create the user account
        new_user = User(
            username=application.username,
            email=application.email,
            user_type="farmer"
        )
        # Set the password from the application
        new_user.password_hash = application.password_hash
        
        db.session.add(new_user)
        
        # Update application status
        application.status = "approved"
        application.reviewed_at = datetime.now()
        # Get admin user ID from session or token if available
        current_user = get_jwt_identity()
        if isinstance(current_user, dict):
            application.reviewed_by = current_user.get('id')
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"Application approved and user account created for '{application.username}'",
            "application": application.to_dict(),
            "user": new_user.to_dict()
        }), 200
        except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Failed to approve application",
            "message": str(e)
        }), 500

@app.route("/api/admin/farmers/applications/<int:application_id>/deny", methods=["POST"])
def deny_farmer_application(application_id):
    """Deny a farmer application"""
    try:
        application = FarmerApplication.query.get(application_id)
        
        if not application:
            return jsonify({
                "success": False,
                "error": "Application not found"
            }), 404
        
        if application.status == "denied":
            return jsonify({
                "success": False,
                "error": "Application is already denied"
            }), 400
        
        if application.status == "approved":
            return jsonify({
                "success": False,
                "error": "Cannot deny an approved application"
            }), 400
        
        # Get denial reason from request body (optional)
        data = request.get_json() or {}
        reason = data.get("reason", "Application denied by admin")
        
        # Update application status
        application.status = "denied"
        application.denial_reason = reason
        application.reviewed_at = datetime.now()
        # Get admin user ID from session or token if available
        try:
            current_user = get_jwt_identity()
            if isinstance(current_user, dict):
                application.reviewed_by = current_user.get('id')
        except:
            pass  # If no JWT token, leave reviewed_by as None
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"Application denied for '{application.username}'",
            "application": application.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Failed to deny application",
            "message": str(e)
        }), 500

        @app.route("/api/admin/farmers/applications/stats", methods=["GET"])
def get_farmer_application_stats():
    """Get statistics about farmer applications for admin dashboard"""
    try:
        total = FarmerApplication.query.count()
        pending = FarmerApplication.query.filter_by(status="pending").count()
        approved = FarmerApplication.query.filter_by(status="approved").count()
        denied = FarmerApplication.query.filter_by(status="denied").count()
        
        return jsonify({
            "success": True,
            "stats": {
                "total": total,
                "pending": pending,
                "approved": approved,
                "denied": denied
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Failed to fetch stats",
            "message": str(e)
        }), 500

@app.route("/api/products", methods=["POST"])
def create_product():
    """Create a new product (farmer only)"""
    try:
        # Check if user is logged in via session
        logged_in = session.get('logged_in', False)
        user_id = session.get('user_id')
        user_type = session.get('user_type')
        
        if not logged_in:
            return jsonify({
                "error": "Not authenticated",
                "message": "Please login first. Make sure you're accessing from http://localhost:5000/test (not file://)",
                "debug": {
                    "logged_in": logged_in,
                    "user_id": user_id,
                    "user_type": user_type,
                    "session_keys": list(session.keys()),
                    "has_session": bool(session)
                }
            }), 401
        
        # Check if user is a farmer
        if user_type != 'farmer':
            return jsonify({
                "error": "Unauthorized",
                "message": "Only farmers can post products",
                "debug": {
                    "user_type": user_type
                }
            }), 403
        
        # Verify user still exists in database
        farmer = User.query.get(user_id)
        if not farmer or farmer.user_type != 'farmer':
            return jsonify({
                "error": "Invalid session",
                "message": "Farmer account not found or invalid"
            }), 403
        
        farmer_id = farmer.id
        
        # Get form data
        name = request.form.get('name')
        description = request.form.get('description', '')
        price = request.form.get('price')
        quantity = request.form.get('quantity')
        unit = request.form.get('unit', 'kg')
        category = request.form.get('category', '')
        location = request.form.get('location', '')
        
        # Validate required fields
        if not name or not price or not quantity:
            return jsonify({
                "error": "Missing required fields",
                "message": "Name, price, and quantity are required"
            }), 400
        
        try:
            price = float(price)
            quantity = float(quantity)
        except ValueError:
            return jsonify({
                "error": "Invalid data",
                "message": "Price and quantity must be numbers"
            }), 400
        
        # Handle photo upload
        photo_filename = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename != '' and allowed_file(file.filename):
                # Generate unique filename
                file_ext = file.filename.rsplit('.', 1)[1].lower()
                photo_filename = f"{uuid4().hex}.{file_ext}"
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
                file.save(file_path)
        
        # Create product
        new_product = Product(
            farmer_id=farmer_id,
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            unit=unit,
            category=category,
            location=location,
            photo_filename=photo_filename
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Product created successfully",
            "product": new_product.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Failed to create product",
            "message": str(e)
        }), 500

@app.route("/api/products/search", methods=["GET"])
def search_products():
    """Search for products by name"""
    try:
        search_query = request.args.get('q', '').strip()
        
        if not search_query:
            return jsonify({
                "error": "Missing search query",
                "message": "Please provide a search query parameter 'q'"
            }), 400
        
        # Search products by name (case-insensitive partial match)
        products = Product.query.filter(
            Product.name.ilike(f'%{search_query}%'),
            Product.is_available == True
        ).all()
        
        return jsonify({
            "success": True,
            "query": search_query,
            "count": len(products),
            "products": [product.to_dict() for product in products]
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Search failed",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
