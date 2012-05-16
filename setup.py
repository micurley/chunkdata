from setuptools import setup, find_packages
from distribute_setup import use_setuptools
use_setuptools()


setup(
    name='chunkdata',
    version='0.2.0',
    author='Aaron McCall',
    author_email='aaron@andyet.net',
    packages=find_packages(),
    url='https://github.com/aaronmccall/chunkdata/',
    license='MIT License',
    description='Chunked fixture tools for Django',
    long_description=open('README.md').read(),
    download_url='https://github.com/aaronmccall/chunkdata/',
    classifiers = [
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                   'Topic :: Internet :: WWW/HTTP :: WSGI',
                   'Topic :: Software Development :: Libraries :: Application Frameworks',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Software Development :: Testing',
                   'Topic :: Utilities',
                   ]

)