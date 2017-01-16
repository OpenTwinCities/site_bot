# -*- coding: utf8 -*-
from subprocess import Popen, PIPE


class GitClient:
    GIT_STATUS_CMD = ['git', 'status', '--porcelain']
    GIT_STAGE_CMD = ['git', 'add', '.']
    GIT_COMMIT_CMD = ['git', 'commit', '-m']
    GIT_PULL_CMD = ['git', 'pull']
    GIT_PUSH_CMD = ['git', 'push']

    def __init__(self, repo_dir, author_name, author_email, author_key):
        self.repo_dir = repo_dir
        self.author = {
            'name': author_name,
            'email': author_email,
            'key': author_key
        }

    def __execute__(self, cmd):
        command = Popen(cmd, cwd=self.repo_dir, stdout=PIPE, stderr=PIPE)
        (stdout, error) = command.communicate()
        if error:
            raise Exception(error)

        return stdout

    @property
    def status(self):
        statuses = self.__execute__(self.GIT_STATUS_CMD)
        statuses = statuses.replace('??', 'A')
        statuses = statuses.split('\n')
        return {filename: status for (status, filename) in statuses.split()}

    def stage_all(self):
        return self.__execute__(self.GIT_STAGE_CMD)

    def pull(self):
        return self.__execute__(self.GIT_PULL_CMD)

    def push(self):
        return self.__execute__(self.GIT_PUSH_CMD)
