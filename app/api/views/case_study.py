from app.api import api
from flask import request, jsonify, current_app
from flask_login import current_user, login_required
from app.api.helpers import not_found, role_required, abort, exception_logger
from app.api.services import (
    evidence_service, evidence_assessment_service, domain_service, suppliers, briefs, assessments,
    domain_criteria_service
)
from app.api.business.validators import EvidenceDataValidator
from app.api.business.case_study_business import get_approved_case_studies
from ...utils import get_json_from_request


@api.route('/case-studies/<int:domain_id>/view', methods=['GET'])
@exception_logger
@login_required
@role_required('supplier')
def get_case_studies(domain_id):
    data = get_approved_case_studies(current_user.supplier_code, domain_id)
    return jsonify(data)
