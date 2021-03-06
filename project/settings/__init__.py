import os.path
import sys

from base import *

# Load settings overides
_path = os.path.join(PROJECT_ROOT, 'settings', 'hosts')
sys.path.insert(0, _path)

from socket import gethostname
_hostname = gethostname().split('.')[0]

_overide_var = 'Django Project' + '_OVERRIDE'
ENV_VAR = _overide_var.replace(' ', '_').upper()

if os.environ.get(ENV_VAR):
    sys.modules['host'] = __import__(os.environ.get(ENV_VAR))
    from host import *
    del sys.modules['host']
elif os.path.isfile(os.path.join(_path,'local_settings.py')):
    from local_settings import *
elif os.path.isfile(os.path.join(_path, '%s.py' % _hostname)):
    sys.modules['host'] = __import__(_hostname)
    from host import *
    del sys.modules['host']

sys.path.remove(_path)

# Any other configuration that should apply to all
# settings versions but relies on other settings (ei: debug)
# should go here.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
           'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'stream' : {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
        'file' : {
            'level' : 'WARNING',
            'class': 'logging.FileHandler',
            'filename': LOG_FILENAME and LOG_FILENAME or '/dev/null',
            'formatter': 'simple'
        }
    },
    'loggers': {
        '': {
            'handlers': DEBUG and ['stream'] or ['mail_admins', 'file'],
            'level': DEBUG and 'DEBUG' or 'WARNING',
            'propagate': True,
        },
    }
}

# URL That doesn't change.
PERM_STATIC_URL = STATIC_URL

version_file = os.path.join(BASE_DIR, 'VERSION')
if os.path.isfile(version_file):
    data = open(version_file, 'r').read().strip()
    if data:
        STATIC_URL = STATIC_URL + 'c-%s/' % data
