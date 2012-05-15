import os
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core import management

try:
    from django.db import DEFAULT_DB_ALIAS
except ImportError:
    DEFAULT_DB_ALIAS = None
from django.db.models import get_apps

class Command(BaseCommand):
    help = 'Installs the named fixture(s) in the database.'
    args = "fixture [fixture ...]"

    option_list = BaseCommand.option_list
    if DEFAULT_DB_ALIAS:
        option_list = option_list + (
            make_option('--database', action='store', dest='database',
                default=DEFAULT_DB_ALIAS, help='Nominates a specific database to load '
                    'fixtures into. Defaults to the "default" database.'),
        )

    def handle(self, *fixture_labels, **options):
        
        app_module_paths = []
        for app in get_apps():
            if hasattr(app, '__path__'):
                # It's a 'models/' subpackage
                for path in app.__path__:
                    app_module_paths.append(path)
            else:
                # It's a models.py module
                app_module_paths.append(app.__file__)

        app_fixtures = [os.path.join(os.path.dirname(path), 'fixtures') for path in app_module_paths]
        final_fixtures = []
        for fixture_label in fixture_labels:
            if os.path.isabs(fixture_label):
                management.call_command('loaddata', *[fixture_label], **options)
            else:
                fixture_dirs = app_fixtures + list(settings.FIXTURE_DIRS) + ['']
                fixture_dirs.sort()
                for fixture_dir in fixture_dirs:
                    filepath = os.path.join(fixture_dir, fixture_label)
                    if os.path.exists(filepath):
                        if os.path.isdir(filepath):
                            for item in os.listdir(filepath):
                                if fixture_label.split('/')[-1] in [item, item.split('.')[0]]:
                                    final_fixtures.append(os.path.join(filepath, item))
                    else:
                        management.call_command('loaddata', *[fixture_label], **options)

        if final_fixtures:
            management.call_command('loaddata', *final_fixtures, **options)