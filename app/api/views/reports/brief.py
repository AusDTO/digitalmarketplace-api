from flask import jsonify
from app.api import api
from app.api.helpers import require_api_key_auth
from app.api.services.reports import briefs_service


@api.route('/reports/brief/published', methods=['GET'])
@require_api_key_auth
def get_published_briefs():
    result = briefs_service.get_published_briefs()
    return jsonify({
        'items': result,
        'total': len(result)
    })
