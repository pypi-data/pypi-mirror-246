"""
reddit-api
"""

from setuptools import setup, find_packages
import re

NAME = 'reddit_api'
PATH_MODULES = 'src/reddit_api'
LONG_DESCRIPTION = 'reddit-api is a open source package that manipulate RedditAPI output and use it in ETL tasks'

def get_version():
    # Read the file and return the version
    with open(f"{PATH_MODULES}/__init__.py") as f:
        version = re.search(r'__version__ = "([^"]+)"', f.read())
        if version:
            return version.group(1)
        else:
            return None
        
# Use the get_version function to retrieve the version
version = get_version()

setup(
    name=NAME,
    version='0.3',
    packages=find_packages(where='src'),
    description='Reddit API for Airflow',
    long_description=LONG_DESCRIPTION,
    author='Unknwon',
    install_requires=[
        'praw',
        'yake',
        'pandas',
        'praw',
        'yake',
        'pyarrow',
        'colorlog'
    ],
    extras_require={
        'dev': [
            'pytest',
            'pytest-cov',
            'flake8',
            'black',
            'isort',
            'mypy',
            'pylint',
            'pre-commit',
            'tox',
            'twine',
            'wheel',
        ]
    },
    package_dir={"": "src"},
    entry_points={
        'console_scripts': [
            'airflow_reddit=airflow_reddit.cli:main',
        ],
    },
)
