from __future__ import unicode_literals

import mock
from flask import current_app
from app.jiraapi import get_api, get_api_oauth, get_marketplace_jira

from .helpers import BaseApplicationTest
from app.models import Application, Supplier, Brief, BriefResponse, Address, Framework, Domain
from app import db


class TestJira(BaseApplicationTest):
    @mock.patch('app.jiraapi.JIRA')
    def test_basic_jira(self, jira):
        with self.app.app_context():
            get_api()
            jira.assert_called_with(
                current_app.config['JIRA_URL'],
                basic_auth=['a', 'b']
            )

    @mock.patch('app.jiraapi.JIRA')
    def test_oauth_jira(self, jira):
        with self.app.app_context():
            get_api_oauth()
            jira.assert_called_with(
                current_app.config['JIRA_URL'],
                oauth={
                    'access_token': 'at',
                    'consumer_key': 'ck',
                    'access_token_secret': 'ats',
                    'key_cert': 'kc'
                }
            )

    @mock.patch('app.jiraapi.get_api_oauth')
    @mock.patch('app.jiraapi.get_api')
    @mock.patch('app.jiraapi.JIRA')
    @mock.patch('app.jiraapi.MarketplaceJIRA')
    def test_create_approval_task(self, MarketplaceJIRA, JIRA, get_api, get_api_oauth):
        with self.app.app_context() as a:
            j = JIRA()
            get_api_oauth.return_value = j

            mj = get_marketplace_jira()

            application = Application(
                id=99,
                status='saved',
                data={'name': 'Umbrella Corporation'}
            )
            domains = db.session.query(Domain).all()
            application.submit_for_approval()
            mj.create_application_approval_task.assert_called_with(application, domains, None)

    @mock.patch('app.jiraapi.get_api_oauth')
    @mock.patch('app.jiraapi.JIRA')
    def test_assessment_tasks_by_application_id(self, JIRA, get_api_oauth):
        with self.app.app_context() as a:
            j = JIRA()
            j.server_info.return_value = {'baseUrl': 'http://jira.example.com'}

            issue_object = mock.Mock()

            issue_object.raw = {
                'fields': {
                    'customfield_11100': 9,
                    'subtasks': [{
                        'id': 99,
                        'key': 'T-99',
                        'fields': {
                            'summary': 'A subtask',
                            'status': {'name': 'Done'}
                        },
                        'self': 'http://api/subissue'
                    }],
                    'summary': 'a task',
                    'status': {'name': 'To Do'}
                },
                'self': 'http://api/topissue',
                'id': 98,
                'key': 'T-98'
            }

            get_api_oauth.return_value = j
            mj = get_marketplace_jira()

            mj.generic_jira.jira.search_issues.return_value = [issue_object]

            assert mj.assessment_tasks_by_application_id() == {
                9: {
                    'id': 98,
                    'key': 'T-98',
                    u'self': u'http://api/topissue',
                    u'link': 'http://jira.example.com/browse/T-98',
                    u'status': u'to-do',
                    u'subtasks': [
                        {
                            'id': 99,
                            'key': 'T-99',
                            u'self': u'http://api/subissue',
                            u'link': 'http://jira.example.com/browse/T-99',
                            u'status': u'done',
                            u'summary': u'A subtask'
                        }
                    ],
                    u'summary': u'a task'
                }
            }
