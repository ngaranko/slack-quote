from sq.settings import *  # noqa: F403


# Only available (and required) for tests, so inject it here.
INSTALLED_APPS = list(INSTALLED_APPS)  # noqa: F405
INSTALLED_APPS.append('django_nose')

INTERNAL_IPS = None

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-coverage',
    '--cover-erase',
    '--cover-html',
    '--cover-html-dir=coverage_report/html',
]
