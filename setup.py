# -*- coding: utf-8 -*-

from setuptools import find_packages, setup

VERSION = __import__('vault').__version__

setup(
    name='vault',
    version=VERSION,
    description='App Django - Interface do Vault',
    author='Storm',
    author_email='storm@g.globo',
    url='https://github.com/globocom/vault'
    install_requires=[
        'Babel==2.3.4',
        'gunicorn==19.3.0',
        'Django==3.0.3',
        'django3-all-access==0.10.0',
        'iso8601==0.1.11',
        'mysqlclient==1.4.6',
        'netaddr==0.7.18',
        'oslo.config==5.2.0',
        'python-dateutil==2.5.3',
        'python-keystoneclient==3.16.0',
        'python-swiftclient==3.7.1',
        'py-zabbix==1.1.5',
        'pytz==2015.4',
        'requests==2.19.1'
    ],
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
)
