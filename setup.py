import os
from setuptools import find_packages
from setuptools import setup

with open(os.path.join('atlassian', 'VERSION')) as file:
    version = file.read().strip()

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='atlassian-python-api',
    description='Python Atlassian REST API Wrapper',
    long_description=long_description,
    license='Apache License 2.0',
    version=version,
    download_url='https://github.com/atlassian-api/atlassian-python-api',

    author='Matt Harasymczuk',
    author_email='matt@astrotech.io',
    url='https://github.com/atlassian-api/atlassian-python-api',
    keywords='atlassian jira confluence bitbucket bamboo crowd portfolio servicedesk jsd rest api',

    packages=find_packages(),
    package_dir={'atlassian': 'atlassian'},
    include_package_data=True,

    zip_safe=False,
    install_requires=[
        'requests',
        'six'
    ],
    platforms='Platform Independent',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks']
)
