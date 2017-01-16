# -*- coding: utf8 -*-
from __future__ import absolute_import
from site_bot_test_helper import SiteBotTestCase
from Git.Client import GitClient
import mock


class GitClientTest(SiteBotTestCase):
    def setUp(self):
        super(GitClientTest, self).setUp()
        self.subject = GitClient('foo/', 'A Name', 'address@example.com')
        self.mock_git_status = "?? path1\n M path/to2\n A path/to/other3"
        self.mock_status = {'path1': 'A',
                            'path/to2': 'M',
                            'path/to/other3': 'A'}

    @mock.patch.object(GitClient, '__execute__')
    def test_status(self, mock_execute):
        mock_execute.return_value = self.mock_git_status
        status = self.subject.status
        mock_execute.assert_called_once_with(['git', 'status', '--porcelain'])
        self.assertEqual(status, self.mock_status)

    @mock.patch.object(GitClient, '__execute__')
    def test_empty_status(self, mock_execute):
        mock_execute.return_value = ''
        status = self.subject.status
        mock_execute.assert_called_once_with(['git', 'status', '--porcelain'])
        self.assertEqual(status, {})

    @mock.patch.object(GitClient, 'status', new_callable=mock.PropertyMock)
    def test_new_files(self, mock_status):
        mock_status.return_value = self.mock_status
        self.assertEqual(self.subject.new_files, ['path1', 'path/to/other3'])

    @mock.patch.object(GitClient, 'status', new_callable=mock.PropertyMock)
    def test_empty_new_files(self, mock_status):
        mock_status.return_value = {}
        self.assertEqual(self.subject.new_files, [])

    @mock.patch.object(GitClient, 'status', new_callable=mock.PropertyMock)
    def test_modified_files(self, mock_status):
        mock_status.return_value = self.mock_status
        self.assertEqual(self.subject.modified_files, ['path/to2'])

    @mock.patch.object(GitClient, 'status', new_callable=mock.PropertyMock)
    def test_empty_modified_files(self, mock_status):
        mock_status.return_value = {}
        self.assertEqual(self.subject.modified_files, [])

    @mock.patch.object(GitClient, 'status', new_callable=mock.PropertyMock)
    def test_message(self, mock_status):
        mock_status.return_value = self.mock_status
        self.assertIn('Added path1', self.subject.message)
        self.assertIn('Updated path/to2', self.subject.message)
        self.assertIn('Added path/to/other3', self.subject.message)
        self.assertEqual(3, len(self.subject.message.split('\n')))

    @mock.patch.object(GitClient, '__execute__')
    def test_stage_all(self, mock_execute):
        self.subject.stage_all()
        mock_execute.assert_called_once_with(['git', 'add', '.'])

    @mock.patch.object(GitClient, '__execute__')
    def test_reset_hard(self, mock_execute):
        mock_execute.return_value = ''
        self.subject.reset_hard()
        mock_execute.assert_has_calls([
            mock.call(['git', 'reset', '--hard', 'HEAD']),
            mock.call(['git', 'clean', '-df'])
        ])

    @mock.patch.object(GitClient, '__execute__')
    @mock.patch.object(GitClient, 'reset_hard')
    def test_remove_head_commit(self, mock_reset_hard, mock_execute):
        mock_execute.return_value = ''
        mock_reset_hard.return_value = ''
        self.subject.remove_head_commit()
        mock_execute.assert_called_once_with(['git', 'reset',
                                              '--hard', 'HEAD~1'])
        mock_reset_hard.assert_called_once

    @mock.patch.object(GitClient, '__execute__')
    @mock.patch.object(GitClient, 'message', new_callable=mock.PropertyMock)
    def test_commit(self, mock_message, mock_execute):
        mock_message.return_value = "This commit\nhappened."
        self.subject.commit()
        mock_execute.assert_called_once_with(
            ['git', 'commit', '-m', 'This commit\nhappened.',
             '--author="A Name <address@example.com>"'])

    @mock.patch.object(GitClient, '__execute__')
    def test_pull(self, mock_execute):
        self.subject.pull()
        mock_execute.assert_called_once_with(['git', 'pull'])

    @mock.patch.object(GitClient, '__execute__')
    def test_push(self, mock_execute):
        self.subject.push()
        mock_execute.assert_called_once_with(['git', 'push'])
