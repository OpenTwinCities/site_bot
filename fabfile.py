from fabric import task


deploy_folder = '/opt/site_bot'
existing_packages_tmp_file = '/tmp/existing_site_bot_python_requirements.txt'


@task
def deploy(c, ref):
    c.run("""
        cd %(deploy_folder)s
        git fetch origin
        git checkout %(ref)s
        # Delete existing dependencies
        pip3 freeze --user > %(existing_packages_tmp_file)s
        pip3 uninstall -y -r %(existing_packages_tmp_file)s
        rm %(existing_packages_tmp_file)s
        # Install dependencies
        pip3 install --user -r requirements.txt
    """ % {"deploy_folder": deploy_folder,
           "ref": ref,
           "existing_packages_tmp_file": existing_packages_tmp_file})
