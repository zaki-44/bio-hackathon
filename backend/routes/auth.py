"""Authentication routes"""
from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import create_access_token
from models import db, User, FarmerApplication
from config import Config
from utils import generate_unique_filename, ensure_directory_exists
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from uuid import uuid4

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user (farmer, transporter, or user)"""
    try:
        # Check if request has file (for farmer certification)
        if request.content_type and 'multipart/form-data' in request.content_type:
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            user_type = request.form.get("user_type", "").lower()
            farm_name = request.form.get("farm_name", "")
            location = request.form.get("location", "")
            phone = request.form.get("phone", "")
            description = request.form.get("description", "")
            certification_file = request.files.get("certification")
        else:
            data = request.get_json()
            username = data.get("username") if data else None
            email = data.get("email") if data else None
            password = data.get("password") if data else None
            user_type = data.get("user_type", "").lower() if data else ""
            farm_name = data.get("farm_name", "")
            location = data.get("location", "")
            phone = data.get("phone", "")
            description = data.get("description", "")
            certification_file = None
        
        # Validate required fields
        if not username or not email or not password:
            return jsonify({
                "error": "Missing required fields",
                "message": "Username, email, and password are required"
            }), 400
        
        if user_type not in Config.VALID_USER_TYPES:
            return jsonify({
                "error": "Invalid user type",
                "message": f"User type must be one of: {', '.join(Config.VALID_USER_TYPES)}"
            }), 400
        
        # For farmers, require certification and create application instead of user
        if user_type == 'farmer':
            if not certification_file:
                return jsonify({
                    "error": "Certification required",
                    "message": "Organic certification document is required for farmer registration"
                }), 400
            
            # Validate file type (PDF only)
            if certification_file.filename.rsplit('.', 1)[1].lower() != 'pdf':
                return jsonify({
                    "error": "Invalid file type",
                    "message": "Certification must be a PDF file"
                }), 400
            
            # Check if application already exists
            existing_application = FarmerApplication.query.filter(
                (FarmerApplication.email == email) | (FarmerApplication.username == username)
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
            
            # Check if user already exists
            if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
                return jsonify({
                    "error": "User already exists",
                    "message": "This username or email is already registered"
                }), 400
            
            # Save certification file
            cert_filename = f"cert_{uuid4().hex}_{secure_filename(certification_file.filename)}"
            cert_path = os.path.join(Config.UPLOAD_FOLDER, 'certifications', cert_filename)
            ensure_directory_exists(os.path.dirname(cert_path))
            certification_file.save(cert_path)
            
            # Create farmer application
            new_application = FarmerApplication(
                username=username,
                email=email,
                farm_name=farm_name or username + "'s Farm",
                location=location or "Not specified",
                phone=phone,
                description=description,
                certification_filename=cert_filename,
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
        
        # For non-farmers, create user directly
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
        
        # Generate access token
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

@auth_bp.route("/login", methods=["POST"])
def login():
    """Login endpoint for farmer, transporter, and user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        username = data.get("username")
        password = data.get("password")
        user_type = data.get("user_type", "").lower()
        
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
        
        # Generate access token
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

@auth_bp.route("/profile", methods=["GET"])
def get_profile():
    """Get current user's profile (session-based)"""
    try:
        if not session.get('logged_in'):
            return jsonify({
                "error": "Not authenticated",
                "message": "Please login first"
            }), 401
        
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

@auth_bp.route("/logout", methods=["POST"])
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

@auth_bp.route("/session", methods=["GET"])
def get_session():
    """Get current session info"""
    logged_in = session.get('logged_in', False)
    return jsonify({
        "logged_in": logged_in,
        "user_id": session.get('user_id'),
        "username": session.get('username'),
        "user_type": session.get('user_type'),
        "session_id": session.get('_id', 'no_id')
    })

