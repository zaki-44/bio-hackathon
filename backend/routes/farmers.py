"""Farmer application routes"""
from flask import Blueprint, jsonify, request, send_from_directory, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth import user_type_required
from models import db, FarmerApplication, User, FarmerRating
from config import Config
from datetime import datetime
import os

farmers_bp = Blueprint('farmers', __name__, url_prefix='/api/farmers')

@farmers_bp.route("/applications/<int:application_id>/certification", methods=["GET"])
@jwt_required()
@user_type_required('admin')
def get_farmer_certification(application_id):
    """Get certification file for a farmer application"""
    try:
        application = FarmerApplication.query.get(application_id)
        
        if not application:
            return jsonify({
                "error": "Application not found"
            }), 404
        
        if not application.certification_filename:
            return jsonify({
                "error": "No certification file found"
            }), 404
        
        cert_path = os.path.join(Config.UPLOAD_FOLDER, 'certifications', application.certification_filename)
        
        if not os.path.exists(cert_path):
            return jsonify({
                "error": "Certification file not found on server"
            }), 404
        
        return send_from_directory(
            os.path.dirname(cert_path),
            os.path.basename(cert_path),
            as_attachment=False,
            mimetype='application/pdf'
        )
    
    except Exception as e:
        return jsonify({
            "error": "Failed to retrieve certification",
            "message": str(e)
        }), 500

@farmers_bp.route("/<int:farmer_id>/rate", methods=["POST"])
def rate_farmer(farmer_id):
    """Rate a farmer (1-5 stars) - requires authentication"""
    try:
        # Check authentication via session or JWT
        user_id = None
        logged_in = session.get('logged_in', False)
        
        if logged_in:
            user_id = session.get('user_id')
        else:
            # Try JWT token
            try:
                identity = get_jwt_identity()
                if isinstance(identity, dict):
                    user_id = identity.get('id')
                else:
                    # If identity is just an ID string
                    user_id = int(identity) if identity else None
            except:
                pass
        
        if not user_id:
            return jsonify({
                "error": "Authentication required",
                "message": "Please login to rate farmers"
            }), 401
        
        # Get user
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                "error": "User not found"
            }), 404
        
        # Get farmer
        farmer = User.query.get(farmer_id)
        if not farmer:
            return jsonify({
                "error": "Farmer not found"
            }), 404
        
        if farmer.user_type != 'farmer':
            return jsonify({
                "error": "Invalid farmer",
                "message": "The specified user is not a farmer"
            }), 400
        
        if farmer.id == user_id:
            return jsonify({
                "error": "Cannot rate yourself",
                "message": "Farmers cannot rate themselves"
            }), 400
        
        # Get rating data
        data = request.get_json()
        rating_value = data.get('rating')
        comment = data.get('comment', '')
        
        # Validate rating
        if not rating_value or not isinstance(rating_value, int):
            return jsonify({
                "error": "Invalid rating",
                "message": "Rating must be an integer between 1 and 5"
            }), 400
        
        if rating_value < 1 or rating_value > 5:
            return jsonify({
                "error": "Invalid rating",
                "message": "Rating must be between 1 and 5 stars"
            }), 400
        
        # Check if user already rated this farmer
        existing_rating = FarmerRating.query.filter_by(
            farmer_id=farmer_id,
            user_id=user_id
        ).first()
        
        if existing_rating:
            # Update existing rating
            existing_rating.rating = rating_value
            existing_rating.comment = comment
            existing_rating.updated_at = datetime.utcnow()
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "Rating updated successfully",
                "rating": existing_rating.to_dict()
            }), 200
        else:
            # Create new rating
            new_rating = FarmerRating(
                farmer_id=farmer_id,
                user_id=user_id,
                rating=rating_value,
                comment=comment
            )
            db.session.add(new_rating)
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "Rating submitted successfully",
                "rating": new_rating.to_dict()
            }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": "Failed to submit rating",
            "message": str(e)
        }), 500

@farmers_bp.route("/<int:farmer_id>/rating", methods=["GET"])
def get_farmer_rating(farmer_id):
    """Get rating information for a farmer"""
    try:
        # Get farmer
        farmer = User.query.get(farmer_id)
        if not farmer:
            return jsonify({
                "error": "Farmer not found"
            }), 404
        
        if farmer.user_type != 'farmer':
            return jsonify({
                "error": "Invalid farmer",
                "message": "The specified user is not a farmer"
            }), 400
        
        # Get user's rating if authenticated
        user_rating = None
        user_id = None
        
        logged_in = session.get('logged_in', False)
        if logged_in:
            user_id = session.get('user_id')
        else:
            try:
                identity = get_jwt_identity()
                if isinstance(identity, dict):
                    user_id = identity.get('id')
                else:
                    user_id = int(identity) if identity else None
            except:
                pass
        
        if user_id:
            user_rating_obj = FarmerRating.query.filter_by(
                farmer_id=farmer_id,
                user_id=user_id
            ).first()
            if user_rating_obj:
                user_rating = user_rating_obj.to_dict()
        
        # Get all ratings
        all_ratings = FarmerRating.query.filter_by(farmer_id=farmer_id).order_by(
            FarmerRating.created_at.desc()
        ).all()
        
        # Calculate statistics
        from sqlalchemy import func
        avg_rating = db.session.query(func.avg(FarmerRating.rating)).filter(
            FarmerRating.farmer_id == farmer_id
        ).scalar()
        
        rating_distribution = {}
        for i in range(1, 6):
            count = FarmerRating.query.filter_by(
                farmer_id=farmer_id,
                rating=i
            ).count()
            rating_distribution[i] = count
        
        return jsonify({
            "success": True,
            "farmer_id": farmer_id,
            "farmer_username": farmer.username,
            "average_rating": round(float(avg_rating), 2) if avg_rating else None,
            "total_ratings": len(all_ratings),
            "rating_distribution": rating_distribution,
            "user_rating": user_rating,
            "ratings": [rating.to_dict() for rating in all_ratings]
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Failed to fetch rating",
            "message": str(e)
        }), 500

@farmers_bp.route("/<int:farmer_id>/ratings", methods=["GET"])
def get_farmer_ratings_list(farmer_id):
    """Get list of all ratings for a farmer (with pagination)"""
    try:
        farmer = User.query.get(farmer_id)
        if not farmer or farmer.user_type != 'farmer':
            return jsonify({
                "error": "Farmer not found"
            }), 404
        
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        per_page = min(per_page, 50)  # Max 50 per page
        
        ratings_query = FarmerRating.query.filter_by(farmer_id=farmer_id).order_by(
            FarmerRating.created_at.desc()
        )
        
        paginated = ratings_query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            "success": True,
            "farmer_id": farmer_id,
            "farmer_username": farmer.username,
            "ratings": [rating.to_dict() for rating in paginated.items],
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": paginated.total,
                "pages": paginated.pages
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": "Failed to fetch ratings",
            "message": str(e)
        }), 500

