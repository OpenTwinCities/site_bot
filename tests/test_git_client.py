# -*- coding: utf8 -*-
from __future__ import absolute_import
from site_bot_test_helper import SiteBotTestCase
from Git.Client import GitClient
import mock


class GitClientTest(SiteBotTestCase):
    def setUp(self):
        super(GitClientTest, self).setUp()
        self.subject = GitClient('foo/', 'Name', 'address@example.com', 'key')

    @mock.patch.object(GitClient, '__execute__')
    def test_status(self, mock_execute):
        self.subject.status
        mock_execute.assert_called_once_with(['git', 'status', '--porcelain'])
