# coding=utf-8
from setuptools import setup

setup(
    name='nmp-model',

    version='4.0',

    description='A data model for NMP by NWPC.',
    long_description=__doc__,

    packages=['nmp_model'],

    include_package_data=True,

    zip_safe=False,

    install_requires=[
        'click',
        'SQLAlchemy',
        'mysql-connector-python',
        'pymongo',
        'mongoengine',
        'PyYAML',
        'redis',
    ],
    extras_require={
        'testing': [
            'pytest',
            'mongomock'
        ]
    }
)
