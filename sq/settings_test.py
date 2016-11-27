from .settings import *


# Only available (and required) for tests, so inject it here.
INSTALLED_APPS = list(INSTALLED_APPS)
INSTALLED_APPS.append('django_nose')

INTERNAL_IPS = None

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-erase',
    '--cover-html',
    '--cover-html-dir=coverage_report/html',
]
