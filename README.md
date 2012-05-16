## What is chunkdata?

Chunkdata is a set of two Django management commands one for creating fixtures and one for loading fixtures.  They are nearly identical in function to dumpdata and loaddata.

## What does chunkdata do that's new?

### Fixture creation
Chunkdata's data dumper `dumpchunks` allows you to specify a maximum object count (`-c` or `--chunk`) per fixture file and an optional fixture file name spec (`-f` or `--filespec`) in addition to `dumpdata`'s normal options. The file spec is used along with increment numbers and output format to construct the filename(s) (and parent directory name if there are multiple chunks) of fixture files written to disk. By default the fixture(s) are output to `app_name/fixtures` if a single app is included or `PWD/fixtures` if not.

The command also observes the following rules regarding chunking models:

1. If the current object count plus the next model to be serialized exceeds the chunk size, the current file will be written and a new file started for the next model.

2. If the current model is being written to multiple files, the last file for the model will be written and a new file started before proceeding to the next model.

#### Examples:
* If you call `django-admin.py dumpchunks -c 10000 -f foo` on a project with a total of 100,000 rows in representing 20 models all of which have 5,000 rows, you will get 10 fixture files like so: 
    ```
    | PWD
    |
    --|fixtures
      |
      --| foo
        |
        |--| foo.1.json
           | foo.2.json
           | foo.3.json
           | foo.4.json
           | foo.5.json
           | ...
           | foo.10.json
    ```

* If you call `django-admin.py dumpchunks -c 10000` on a project with a total of 15,000 rows representing two models `Foo` and `Bar` in a single `main` app, you will get three fixture files like so:
    ```
    | PROJECT_ROOT
    |
    --|main
      |
      --| fixtures
        |
        |--| main
           |
           --| main.1.json
             | main.2.json
             | main.3.json
    ```

### Fixture loading
Chunkdata's data loader `loadchunks` follows the loaddata API and it will find all of the chunks automatically--if there is a directory that matches the name and it contains files matching the pattern `(name)\.(\d+)\.(json|yaml|xml)`. If there are no chunks, it functions identically to Django's loaddata.

### Testing
Chunkdata comes with a Django project for testing at `testproject`. In order to run the tests, either install the pip requirements to a virtualenv or have Django available on your global Python path. then run `python manage.py test` from the `testproject` directory.