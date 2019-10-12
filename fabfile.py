from fabric import task


deploy_folder = '/opt/site_bot'


@task
def deploy(c, ref='master'):
    c.run("""
        cd %s
        git fetch origin
        git checkout %s""" % (deploy_folder, ref))
