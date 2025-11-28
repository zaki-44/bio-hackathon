from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def user_type_required(*allowed_types):
    """
    Decorator to restrict access to specific user types.
    Usage: @user_type_required('farmer', 'transporter')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            current_user = get_jwt_identity()
            
            if current_user.get('user_type') not in allowed_types:
                return jsonify({
                    'error': 'Insufficient permissions',
                    'message': f'This endpoint requires one of the following user types: {", ".join(allowed_types)}'
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

