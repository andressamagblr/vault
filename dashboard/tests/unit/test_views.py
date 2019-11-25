# -*- coding: utf-8 -*-

from unittest import TestCase
from mock import Mock, patch

from vault.tests.fakes import fake_request
from dashboard.views import DashboardView


class DashboardTest(TestCase):

    def setUp(self):
        self.view = DashboardView.as_view()
        self.request = fake_request(method='GET')
        self.request.META.update({
            'SERVER_NAME': 'globo.com',
            'SERVER_PORT': '80',
            'HTTP_HOST': 'localhost'
        })
        self.request.user.is_authenticated.value = True

        # silence logs
        patch('dashboard.widgets.log', Mock(return_value=None)).start()

        # Don't render widgets
        patch('dashboard.templatetags.dashboard_tags.RenderWidgets.render',
              Mock(return_value="")).start()

        # does not connect to the keystone client
        patch('keystoneclient.v2_0.client.Client').start()

    def tearDown(self):
        patch.stopall()

    def test_dashboard_needs_authentication(self):
        self.request.user.is_authenticated.value = False
        response = self.view(self.request)
        self.assertEqual(response.status_code, 302)

    def test_show_dashboard(self):
        response = self.view(self.request)
        self.assertEqual(response.status_code, 200)

        response.render()
        self.assertIn('Dashboard', response.content)
