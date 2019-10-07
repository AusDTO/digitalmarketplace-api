from flask import jsonify, abort, current_app, request
from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import aggregate_order_by
from app.api.helpers import Service
from app.models import Team, TeamMember, TeamMemberPermission, User, db

from app.api.business import (team_business)
from app.tasks import publish_tasks
from .. import main
from ... import db
from ...models import (
    User,
    Brief,
    TeamBrief,
    Team
)
from ...utils import (
    get_json_from_request, get_int_or_400, json_has_required_keys, pagination_links,
    get_valid_page_or_1, get_request_page_questions, validate_and_return_updater_request,
    get_positive_int_or_400
)
from ...service_utils import validate_and_return_lot, filter_services

from ...datetime_utils import parse_time_of_day, combine_date_and_time


@main.route('/admin/team/<int:team_id>', methods=['GET'])
def get_team(team_id):
    team = team_business.get_team(team_id, True)
    briefs = team_business.get_team_briefs(team_id)
    return jsonify(team=team, briefs=briefs)


@main.route('/admin/buyers/<int:brief_id>/teams', methods=['GET'])
def brief_exists_in_teams(brief_id):
    return jsonify(team_business.is_brief_id_in_teams(brief_id))
