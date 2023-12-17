from setuptools import setup, find_packages

setup(
    name='tlylt',
    version='0.0.1',
    author='Liu Yongliang',
    author_email='liu_yongliang@hotmail.com',
    description='A collection of scripts for daily use.',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'tlylt=tlylt.scripts.cli:app',
        ],
    },
)
