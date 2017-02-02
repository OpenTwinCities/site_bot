# -*- coding: utf8 -*-
import copy
from subprocess import Popen, PIPE


class GitClient:
    GIT_STATUS_CMD = ['git', 'status', '--porcelain']
    GIT_STAGE_CMD = ['git', 'add', '.']
    GIT_RESET_HARD_CMD = ['git', 'reset', '--hard', 'HEAD']
    GIT_REMOVE_HEAD_COMMIT_CMD = ['git', 'reset', '--hard', 'HEAD~1']
    GIT_CLEAN_CMD = ['git', 'clean', '-df']
    GIT_COMMIT_CMD = ['git', 'commit', '-m']
    GIT_PULL_CMD = ['git', 'pull', '--force']
    GIT_PUSH_CMD = ['git', 'push', '--quiet']

    def __init__(self, repo_dir, author_name, author_email):
        self.repo_dir = repo_dir
        self.author = {
            'name': author_name,
            'email': author_email
        }

    def __execute__(self, cmd):
        command = Popen(cmd, cwd=self.repo_dir, stdout=PIPE, stderr=PIPE)
        (stdout, error) = command.communicate()
        if error:
            raise Exception(error)

        return stdout

    @property
    def status(self):
        '''A dict of paths that differ in some what from HEAD. The value
        associated with each path is a git status code indicated the type of
        difference.'''

        def transform(status):
            status = status.strip()
            if status.startswith('R'):
                return status.split(' ', 1)
            else:
                return status.split()

        statuses = self.__execute__(self.GIT_STATUS_CMD)
        statuses = statuses.replace('??', 'A')
        statuses = [status for status in
                    [transform(status) for status in statuses.split('\n')]
                    if status]
        if statuses:
            return {path: code for (code, path) in statuses}
        else:
            return {}

    @property
    def new_files(self):
        '''A list of paths to new files that are not current in HEAD.'''
        return [path for (path, code) in self.status.iteritems()
                if code == 'A']

    @property
    def modified_files(self):
        '''A list of paths to existing files in HEAD that have been
        modified.'''
        return [path for (path, code) in self.status.iteritems()
                if code == 'M']

    @property
    def renamed_files(self):
        '''A list of paths to existing files in HEAD that have been
        renamed/moved.'''
        return [path for (path, code) in self.status.iteritems()
                if code == 'R']

    @property
    def message(self):
        '''Message summarizing what is to be commited.'''
        return '\n'.join(['Added %s' % path for path in self.new_files] +
                         ['Updated %s' % path
                          for path in self.modified_files] +
                         ['Renamed %s' % path for path in self.renamed_files])

    def stage_all(self):
        return self.__execute__(self.GIT_STAGE_CMD)

    def commit(self):
        commit_cmd = copy.deepcopy(self.GIT_COMMIT_CMD)
        commit_cmd.append(self.message)
        commit_cmd.append('--author="%s <%s>"' % (self.author['name'],
                                                  self.author['email']))
        return self.__execute__(commit_cmd)

    def reset_hard(self):
        '''Does a hard reset of the repo to HEAD, and a clean'''
        return '\n'.join([self.__execute__(self.GIT_RESET_HARD_CMD),
                          self.__execute__(self.GIT_CLEAN_CMD)])

    def remove_head_commit(self):
        '''Resets the repo to the current HEAD's parent.'''
        return '\n'.join([self.__execute__(self.GIT_REMOVE_HEAD_COMMIT_CMD),
                          self.reset_hard()])

    def pull(self):
        return self.__execute__(self.GIT_PULL_CMD)

    def push(self):
        return self.__execute__(self.GIT_PUSH_CMD)
