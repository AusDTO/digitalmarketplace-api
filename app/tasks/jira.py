from flask import current_app

from app.api.services import (AuditTypes, application_service, assessments,
                              audit_service, domain_service,
                              suppliers, evidence_service)
from app.emails import (send_approval_notification,
                        send_assessment_approval_notification)
from app.jiraapi import get_marketplace_jira
from . import celery


@celery.task
def create_evidence_assessment_in_jira(evidence_id):
    evidence = evidence_service.get_evidence_by_id(evidence_id)
    if not evidence:
        return False

    marketplace_jira = get_marketplace_jira()
    marketplace_jira.create_evidence_approval_task(evidence)


@celery.task
def sync_application_approvals_with_jira():
    application_ids = application_service.get_submitted_application_ids()

    marketplace_jira = get_marketplace_jira()
    response = marketplace_jira.find_approved_application_issues(application_ids)

    application_id_field = current_app.config['JIRA_FIELD_CODES'].get('APPLICATION_FIELD_CODE')

    for issue in response['issues']:
        application_id = int(issue['fields'][application_id_field])
        application = application_service.get(application_id)
        if application and application.status == 'submitted':
            audit_service.log_audit_event(
                audit_type=AuditTypes.approve_application,
                user='Sync application approvals with Jira task',
                data={'jira_issue_key': issue['key']},
                db_object=application
            )

            application.set_approval(approved=True)
            application_service.commit_changes()
            send_approval_notification(application_id)
