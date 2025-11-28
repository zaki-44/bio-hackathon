"""Admin routes"""
from flask import Blueprint, jsonify, request, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import user_type_required
from models import db, User, FarmerApplication
from config import Config
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route("/farmers/applications", methods=["GET"])
@jwt_required()
@user_type_required('admin')
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

@admin_bp.route("/farmers/applications/<int:application_id>/approve", methods=["POST"])
@jwt_required()
@user_type_required('admin')
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
                # If no JWT token, try to get from session
                try:
                    if session.get('user_id'):
                        application.reviewed_by = session.get('user_id')
                except:
                    pass
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
        try:
            current_user = get_jwt_identity()
            if isinstance(current_user, dict):
                application.reviewed_by = current_user.get('id')
        except:
            # If no JWT token, try to get from session
            try:
                if session.get('user_id'):
                    application.reviewed_by = session.get('user_id')
            except:
                pass
        
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

@admin_bp.route("/farmers/applications/<int:application_id>/deny", methods=["POST"])
@jwt_required()
@user_type_required('admin')
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
            try:
                if session.get('user_id'):
                    application.reviewed_by = session.get('user_id')
            except:
                pass
        
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

@admin_bp.route("/farmers/applications/stats", methods=["GET"])
@jwt_required()
@user_type_required('admin')
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

@admin_bp.route("/create-admin", methods=["POST"])
def create_admin_user():
    """Create an admin user (for initial setup)"""
    try:
        data = request.get_json()
        
        username = data.get("username", "admin")
        email = data.get("email", "admin@biomarket.com")
        password = data.get("password", "admin123")
        
        # Check if admin already exists
        existing_admin = User.query.filter_by(user_type='admin').first()
        if existing_admin:
            return jsonify({
                "error": "Admin already exists",
                "message": "An admin user already exists in the system"
            }), 400
        
        # Check if username or email already exists
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
        
        # Create admin user
        admin_user = User(
            username=username,
            email=email,
            user_type='admin'
        )
        admin_user.set_password(password)
        
        db.session.add(admin_user)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": f"Admin user '{username}' created successfully",
            "user": admin_user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Failed to create admin",
            "message": str(e)
        }), 500

