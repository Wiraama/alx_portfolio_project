from flask import jsonify, render_template, Blueprint

error_bp = Blueprint('errors', __name__)

@error_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@error_bp.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

@error_bp.app_errorhandler(403)
def forbidden_error(error):
    return render_template('403.html'), 403

@error_bp.app_errorhandler(400)
def bad_request(error):
    res = {
            "error": "Bad Request",
            "message": str(error)
            }
     
    return jsonify(res), 400
