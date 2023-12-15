"""
reddit-api
"""

from setuptools import setup, find_packages

LONG_DESCRIPTION = 'reddit-api is a open source package that manipulate RedditAPI output and use it in ETL tasks'


setup(
    name='reddit_api',
    version='0.1',
    packages=find_packages(where='src'),
    description='Reddit API for Airflow',
    long_description=LONG_DESCRIPTION,
    author='Unknwon',
    install_requires=[
        'praw',
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
