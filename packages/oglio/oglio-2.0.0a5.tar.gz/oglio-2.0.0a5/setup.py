import pathlib
from setuptools import setup
from oglio import __version__ as oglioVersion

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()
LICENSE = (HERE / 'LICENSE').read_text()

setup(
    name="oglio",
    version=oglioVersion,
    author_email='Humberto.A.Sanchez.II@gmail.com',
    maintainer='Humberto A. Sanchez II',
    maintainer_email='humberto.a.sanchez.ii@gmail.com',
    description='External Pyut Persistence',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/hasii2011/oglio",
    packages=[
        'oglio', 'oglio.toXmlV10', 'oglio.toXmlV11'
    ],
    package_data={
        'oglio':          ['py.typed'],
        'oglio.toXmlV10': ['py.typed'],
        'oglio.toXmlV11': ['py.typed'],
    },
    install_requires=[
        'wxPython==4.2.1',
        'codeallybasic==0.5.2',
        'codeallyadvanced==0.5.2',
        'pyutmodelv2==2.0.0a5',
        'ogl==2.0.0a5',
        'untanglepyut==2.0.0a5'
    ],
)
