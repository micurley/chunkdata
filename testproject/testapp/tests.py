from django.core import management
from StringIO import StringIO
from models import TestPerson, TestLocation
from chunkdata.management.commands import loadchunks

from django.test import TestCase

class TestLoadChunks(TestCase):

    def test_normal_fixture_imported_properly(self):
        """ loadchunks should delegate to loaddata when not a chunked fixture
        """
        management.call_command('loadchunks', 'test_dump')

        self.failUnlessEqual(TestPerson.objects.all().count(), 1000)

        self.failUnlessEqual(TestLocation.objects.all().count(), 1013)


    def test_chunked_fixture_imported_properly(self):
        """ loadchunks should find and import all relevant fixtures
        """
        TestPerson.objects.all().delete()

        TestLocation.objects.all().delete()

        self.failUnlessEqual(TestPerson.objects.all().count(), 0)

        self.failUnlessEqual(TestLocation.objects.all().count(), 0)

        management.call_command('loadchunks', 'chunks')

        self.failUnlessEqual(TestPerson.objects.all().count(), 1013)

        self.failUnlessEqual(TestLocation.objects.all().count(), 1000)

    def test_multiple_fixtures_found_raises_error(self):
        """ loadchunks should raise an error when it finds multiple chunked fixtures that match app_label
        """
        self.assertRaises(
            loadchunks.MultipleFixturesFoundError,
            management.call_command,
            *['loadchunks', 'fake_chunks'],
            **{'traceback': True}
        )
        
