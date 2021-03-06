import os

# Register custom serializer for Celery that allows for encoding and decoding
# Python datetime objects (and potentially other ones)
from kombu.serialization import register
from serializers import encoder, decoder

register('ocd_serializer', encoder, decoder, content_encoding='binary',
         content_type='application/ocd-msgpack')

CELERY_CONFIG = {
    'BROKER_URL': 'redis://127.0.0.1:6379/0',
    'CELERY_ACCEPT_CONTENT': ['ocd_serializer'],
    'CELERY_TASK_SERIALIZER': 'ocd_serializer',
    'CELERY_RESULT_SERIALIZER': 'ocd_serializer',
    'CELERY_RESULT_BACKEND': 'ocd_backend.result_backends:OCDRedisBackend+redis://127.0.0.1:6379/0',
    'CELERY_IGNORE_RESULT': True,
    'CELERY_DISABLE_RATE_LIMITS': True,
    # Expire results after 30 minutes; otherwise Redis will keep
    # claiming memory for a day
    'CELERY_TASK_RESULT_EXPIRES': 1800
}

LOGGING = {
    'version': 1,
    'formatters': {
        'console': {
            'format': '[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'console',
            'filename': 'backend.log'
        }
    },
    'loggers': {
        'ocd_backend': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}

ELASTICSEARCH_HOST = '127.0.0.1'
ELASTICSEARCH_PORT = 9200

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# The path of the directory used to store temporary files
TEMP_DIR_PATH = os.path.join(ROOT_PATH, 'temp')

# The path of the JSON file containing the sources config
SOURCES_CONFIG_FILE = os.path.join(ROOT_PATH, 'sources.json')

# The name of the index containing documents from all sources
COMBINED_INDEX = 'ocd_combined_index'

# The default prefix used for all ocd data
DEFAULT_INDEX_PREFIX = 'ocd'

RESOLVER_BASE_URL = 'http://localhost:5000/v0/resolve'
RESOLVER_URL_INDEX = 'ocd_resolver'

# The User-Agent that is used when retrieving data from external sources
USER_AGENT = 'OpenCultuurData/0.1 (+http://www.opencultuurdata.nl/)'

# Allow any settings to be defined in local_settings.py which should be
# ignored in your version control system allowing for settings to be
# defined per machine.
try:
    from local_settings import *
except ImportError:
    pass
