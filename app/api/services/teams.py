from sqlalchemy import and_, func, cast, desc
from sqlalchemy.types import TEXT

from app.api.helpers import Service
from app.models import Team, TeamMember, TeamMemberPermission, User, db


class TeamService(Service):
    __model__ = Team

    def __init__(self, *args, **kwargs):
        super(TeamService, self).__init__(*args, **kwargs)

    def get_teams_for_user(self, user_id, status='completed'):
        return (db.session
                  .query(Team)
                  .filter(Team.status == status)
                  .join(TeamMember, TeamMember.user_id == user_id)
                  .all())

    def get_team(self, team_id):
        team_leads = (db.session
                        .query(TeamMember.team_id, TeamMember.user_id, User.name, User.email_address)
                        .join(Team, Team.id == TeamMember.team_id)
                        .join(User, User.id == TeamMember.user_id)
                        .filter(Team.id == team_id,
                                TeamMember.is_team_lead.is_(True))
                        .subquery('team_leads'))

        aggregated_team_leads = (db.session
                                   .query(team_leads.columns.team_id,
                                          func.json_object_agg(
                                              team_leads.columns.user_id,
                                              func.json_build_object(
                                                  'emailAddress', team_leads.columns.email_address,
                                                  'name', team_leads.columns.name
                                              )
                                          ).label('teamLeads'))
                                   .group_by(team_leads.columns.team_id)
                                   .subquery('aggregated_team_leads'))

        team_member_permissions = (db.session
                                     .query(
                                         TeamMember.team_id,
                                         TeamMember.user_id,
                                         TeamMemberPermission.permission)
                                     .join(Team, Team.id == TeamMember.team_id)
                                     .join(TeamMemberPermission, TeamMemberPermission.team_member_id == TeamMember.id)
                                     .filter(Team.id == team_id,
                                             TeamMember.is_team_lead.is_(False))
                                     .group_by(
                                         TeamMember.team_id,
                                         TeamMember.user_id,
                                         TeamMemberPermission.permission)
                                     .subquery('team_member_permissions'))

        aggregated_permissions = (db.session
                                    .query(
                                        team_member_permissions.columns.team_id,
                                        team_member_permissions.columns.user_id,
                                        func.json_object_agg(
                                            team_member_permissions.columns.permission, True
                                        ).label('permissions'))
                                    .group_by(
                                        team_member_permissions.columns.team_id,
                                        team_member_permissions.columns.user_id)
                                    .subquery('aggregated_permissions'))

        aggregated_team_members = (db.session
                                     .query(TeamMember.team_id,
                                            func.json_object_agg(
                                                TeamMember.user_id,
                                                func.json_build_object(
                                                    'emailAddress', User.email_address,
                                                    'name', User.name,
                                                    'permissions',
                                                    func.coalesce(aggregated_permissions.columns.permissions, '{}')
                                                )).label('teamMembers'))
                                     .join(User, User.id == TeamMember.user_id)
                                     .join(aggregated_permissions,
                                           and_(
                                               aggregated_permissions.columns.team_id == TeamMember.team_id,
                                               aggregated_permissions.columns.user_id == TeamMember.user_id
                                           ), isouter=True)
                                     .filter(TeamMember.team_id == team_id,
                                             TeamMember.is_team_lead.is_(False))
                                     .group_by(TeamMember.team_id)
                                     .subquery('aggregated_team_members'))

        team = (db.session
                  .query(Team.id, Team.name, Team.email_address.label('emailAddress'), Team.status,
                         aggregated_team_leads.columns.teamLeads, aggregated_team_members.columns.teamMembers)
                  .join(aggregated_team_leads, aggregated_team_leads.columns.team_id == Team.id, isouter=True)
                  .join(aggregated_team_members, aggregated_team_members.columns.team_id == Team.id, isouter=True)
                  .filter(Team.id == team_id)
                  .one_or_none())

        return team._asdict() if team else None

    def get_user_teams(self, user_id):
        result = (
            db
            .session
            .query(
                Team.id,
                Team.name,
                TeamMember.is_team_lead,
                func.array_agg(cast(TeamMemberPermission.permission, TEXT)).label('permissions')
            )
            .join(TeamMember)
            .join(TeamMemberPermission, isouter=True)
            .filter(TeamMember.user_id == user_id)
            .filter(Team.status == 'completed')
            .group_by(Team.id, Team.name, TeamMember.is_team_lead)
            .all()
        )
        return [r._asdict() for r in result]

    def get_team_overview(self, team_id, user_id):
        team_members = (db.session
                          .query(User.id, User.name, TeamMember.team_id)
                          .join(TeamMember, TeamMember.user_id == User.id)
                          .filter(TeamMember.team_id == team_id)
                          .order_by(
                              TeamMember.team_id,
                              desc(TeamMember.is_team_lead),
                              User.name)
                          .subquery('team_members'))

        aggregated_team_members = (db.session
                                     .query(team_members.columns.team_id,
                                            func.json_agg(
                                                team_members.columns.name
                                            ).label('members'))
                                     .group_by(team_members.columns.team_id)
                                     .subquery('aggregated_team_members'))

        team = (db.session
                  .query(aggregated_team_members.columns.members, Team.id, Team.name)
                  .join(Team, Team.id == aggregated_team_members.columns.team_id)
                  .filter(Team.status == 'completed')
                  .subquery('team'))

        result = (db.session
                    .query(
                        func.json_build_object(
                            team.columns.id,
                            func.json_build_object(
                                'isTeamLead', TeamMember.is_team_lead,
                                'members', team.columns.members,
                                'name', team.columns.name
                            )
                        ).label('overview'))
                    .join(team, TeamMember.team_id == team.columns.id)
                    .filter(
                        TeamMember.team_id == team_id,
                        TeamMember.user_id == user_id)
                    .one_or_none())

        return result._asdict() if result else None