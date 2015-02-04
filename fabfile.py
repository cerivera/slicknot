from fabric.api import env, run, cd

USERNAME = 'ubuntu'
SERVER = '54.153.66.189'
APP_NAME = 'slicknot'
PROJECT_DIR = '/www/%s' % (APP_NAME)
WSGI_SCRIPT = 'application.wsgi'

env.hosts = ["%s@%s" % (USERNAME, SERVER)]

def deploy():
    with cd(PROJECT_DIR):
        run('git pull')
        run('bin source/activate')
        run('pip install -r requirements.txt')
        run('touch %s' % WSGI_SCRIPT)
