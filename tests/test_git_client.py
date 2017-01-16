# -*- coding: utf8 -*-
from __future__ import absolute_import
from site_bot_test_helper import SiteBotTestCase
from Git.Client import GitClient
import mock


class GitClientTest(SiteBotTestCase):
    def setUp(self):
        super(GitClientTest, self).setUp()
        self.subject = GitClient('foo/', 'Name', 'address@example.com')
        self.mock_git_status = "?? path1\n M path/to2\n A path/to/other3"

    @mock.patch.object(GitClient, '__execute__')
    def test_status(self, mock_execute):
        mock_execute.return_value = self.mock_git_status
        status = self.subject.status
        mock_execute.assert_called_once_with(['git', 'status', '--porcelain'])
        self.assertEqual(status, {'path1': 'A',
                                  'path/to2': 'M',
                                  'path/to/other3': 'A'})

    @mock.patch.object(GitClient, '__execute__')
    def test_empty_status(self, mock_execute):
        mock_execute.return_value = ''
        status = self.subject.status
        mock_execute.assert_called_once_with(['git', 'status', '--porcelain'])
        self.assertEqual(status, {})

    @mock.patch.object(GitClient, '__execute__')
    def test_new_files(self, mock_execute):
        mock_execute.return_value = self.mock_git_status
        new_files = self.subject.new_files
        mock_execute.assert_called_once_with(['git', 'status', '--porcelain'])
        self.assertEqual(new_files, ['path1', 'path/to/other3'])

    @mock.patch.object(GitClient, '__execute__')
    def test_empty_new_files(self, mock_execute):
        mock_execute.return_value = ''
        new_files = self.subject.new_files
        mock_execute.assert_called_once_with(['git', 'status', '--porcelain'])
        self.assertEqual(new_files, [])

    @mock.patch.object(GitClient, '__execute__')
    def test_modified_files(self, mock_execute):
        mock_execute.return_value = self.mock_git_status
        modified_files = self.subject.modified_files
        mock_execute.assert_called_once_with(['git', 'status', '--porcelain'])
        self.assertEqual(modified_files, ['path/to2'])

    @mock.patch.object(GitClient, '__execute__')
    def test_empty_modified_files(self, mock_execute):
        mock_execute.return_value = ''
        modified_files = self.subject.modified_files
        mock_execute.assert_called_once_with(['git', 'status', '--porcelain'])
        self.assertEqual(modified_files, [])

    @mock.patch.object(GitClient, '__execute__')
    def test_pull(self, mock_execute):
        self.subject.pull()
        mock_execute.assert_called_once_with(['git', 'pull'])

    @mock.patch.object(GitClient, '__execute__')
    def test_push(self, mock_execute):
        self.subject.push()
        mock_execute.assert_called_once_with(['git', 'push'])
