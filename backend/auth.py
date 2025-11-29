from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt

def user_type_required(*allowed_types):
    """
    Decorator to restrict access to specific user types.
    Usage: @user_type_required('farmer', 'transporter')
    Note: Must be used after @jwt_required()
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get JWT claims which contain user_type
            jwt_data = get_jwt()
            user_type = jwt_data.get('user_type')
            
            # If user_type is not in claims, try to get from identity (for backward compatibility)
            if not user_type:
                current_user = get_jwt_identity()
                if isinstance(current_user, dict):
                    user_type = current_user.get('user_type')
            
            if not user_type:
                return jsonify({
                    'error': 'Invalid token format',
                    'message': 'Token does not contain user_type information'
                }), 401
            
            if user_type not in allowed_types:
                return jsonify({
                    'error': 'Insufficient permissions',
                    'message': f'This endpoint requires one of the following user types: {", ".join(allowed_types)}'
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

