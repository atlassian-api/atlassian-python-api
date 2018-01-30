import os
import sys
from setuptools import find_packages
from setuptools import setup

version_file = os.path.join('atlassian', 'VERSION')

assert sys.version_info >= (3, 2), 'Python 3.2+ required.'

setup(
    name='atlassian-python-api',
    description='Python Atlassian REST API Wrapper',
    long_description='Python Atlassian REST API Wrapper',
    license='Apache License 2.0',
    version=open(version_file, 'r').read().strip(),
    download_url='https://github.com/MattAgile/atlassian-python-api',

    author='Matt Harasymczuk',
    author_email='code@mattagile.com',
    url='http://mattagile.com/',

    packages=find_packages(),
    package_dir={'atlassian': 'atlassian'},
    include_package_data=True,

    zip_safe=False,
    install_requires=['requests>=2.7.0'],
    platforms='Platform Independent',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks']
)

