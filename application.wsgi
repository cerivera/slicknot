import os, sys

PROJECT_DIR = '/home/vagrant/slicknot'

activate = os.path.join(PROJECT_DIR, 'bin', 'activate.py')

execfile(activate, dict(__file__=activate))

sys.path.append(PROJECT_DIR)

from slicknot import app as application
