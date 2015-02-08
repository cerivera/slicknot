from __future__ import with_statement
from fabric.api import *
from contextlib import contextmanager as _contextmanager

WSGI_SCRIPT = 'application.wsgi'
PROJECT_DIR = '/www/slicknot'

env.hosts = ['54.153.81.57']
env.user = 'ubuntu'
env.forward_agent = True
env.keyfile = ['%s/keys/Saas2.pem' % (PROJECT_DIR)]
env.directory = PROJECT_DIR
env.activate = 'source %s/bin/activate' % PROJECT_DIR

@_contextmanager
def virtualenv():
    with cd(env.directory):
        with prefix(env.activate):
            yield

def deploy():
    with virtualenv():
        run('git pull')
        run('pip install -r requirements.txt')
        run('touch %s' % WSGI_SCRIPT)
