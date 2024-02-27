
from setuptools import setup

# List of dependencies installed via `pip install -e .`
# by virtue of the Setuptools `install_requires` value below.
requires = [
    'paste==3.5.0',
    'psycopg2-binary>=2.9.3',
    'pyramid>=2.0',
    'pyramid_mako==1.1.0',
    'waitress==2.1.1',
    'alembic==1.7.7',
]

# List of dependencies installed via `pip install -e ".[dev]"`
# by virtue of the Setuptools `extras_require` value in the Python
# dictionary below.

dev_requires = [
    'pyramid_debugtoolbar',
    'beautifulsoup4'
]



setup(
    name='getavax',
    install_requires=requires,
    extras_require={
        'dev': dev_requires,
    },
    entry_points={
        'paste.app_factory': [
            'admin = getavax.admin:main',
            'customer = getavax.customer:main',
            'ersapi = getavax.ersapi:main',
            'root = getavax.root:main',
        ],
    },
    packages = [ 'getavax' ],
)

