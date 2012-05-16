from StringIO import StringIO
import os, json, shutil

from django.core import management
from django.test import TestCase

from models import TestPerson, TestLocation
from chunkdata.management.commands import loadchunks, dumpchunks


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

        self.failUnlessEqual(TestPerson.objects.all().count(), 1000)

        self.failUnlessEqual(TestLocation.objects.all().count(), 1013)

    def test_multiple_fixtures_found_raises_error(self):
        """ loadchunks should raise an error when it finds multiple chunked fixtures that match app_label
        """
        self.assertRaises(
            loadchunks.MultipleFixturesFoundError,
            management.call_command,
            *['loadchunks', 'fake_chunks'],
            **{'traceback': True}
        )
        
class TestDumpChunks(TestCase):
    fixtures = ['test_dump']

    def test_no_chunks_when_no_chunk_arg(self):

        dc = dumpchunks.Command()
        out_json = dc.handle('testapp')
        out_list = json.loads(out_json)
        self.assertEqual(len(out_list), 2013)

    def test_chunks_respect_model_boundaries(self):

        management.call_command('dumpchunks', 'testapp', chunk=300)

        fixtures_path = os.path.join(os.path.dirname(__file__), 'fixtures')
        self.assertTrue(os.path.exists(fixtures_path))

        chunk_dir = os.path.join(fixtures_path, 'testapp')
        chunk_dir_exists = os.path.exists(chunk_dir)
        self.assertTrue(chunk_dir_exists)

        file_list = os.listdir(chunk_dir)
        self.assertEqual(len(file_list), 8)

        last_person_file = os.path.join(chunk_dir, 'testapp.4.json')
        if os.path.exists(last_person_file):
            ppl = json.loads(open(last_person_file).read())
            self.assertEqual(len(ppl), 100)

            person = ppl.pop()
            self.assertEqual(person.get('pk'), 1000)

        if chunk_dir_exists:
            shutil.rmtree(chunk_dir)
