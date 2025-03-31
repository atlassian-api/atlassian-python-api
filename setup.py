import os
from setuptools import find_packages
from setuptools import setup

with open(os.path.join("atlassian", "VERSION")) as file:
    version = file.read().strip()

with open("README.rst") as file:
    long_description = file.read()


setup(
    name="atlassian-python-api",
    description="Python Atlassian REST API Wrapper",
    long_description=long_description,
    license="Apache License 2.0",
    version=version,
    download_url="https://github.com/atlassian-api/atlassian-python-api",
    author="Matt Harasymczuk",
    author_email="matt@astrotech.io",
    maintainer="Gonchik Tsymzhitov",
    maintainer_email="gonchik.tsymzhitov@gmail.com",
    url="https://github.com/atlassian-api/atlassian-python-api",
    keywords="atlassian jira core software confluence bitbucket bamboo crowd portfolio tempo servicedesk assets api",
    packages=find_packages(include=["atlassian*"]),
    package_dir={"atlassian": "atlassian"},
    include_package_data=True,
    zip_safe=False,
    install_requires=["deprecated", "requests", "six", "oauthlib", "requests_oauthlib", "jmespath", "beautifulsoup4", "typing-extensions"],
    extras_require={"kerberos": ["requests-kerberos"]},
    platforms="Platform Independent",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
