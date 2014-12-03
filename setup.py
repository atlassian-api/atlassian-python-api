import sys
from setuptools import setup


assert sys.version_info >= (2, 7), "Python 2.7+ required."

setup(
    name="atlassian-python-api",
    description="Atlassian Python API",
    license="Apache License 2.0",
    version="0.3.3",
    download_url="https://github.com/MattAgile/atlassian-python-api",

    author="Matt Harasymczuk",
    author_email="code@mattagile.com",
    url="http://mattagile.com/",

    packages=["atlassian"],
    package_data={"": ["LICENSE", "README"], "atlassian": ["*.py"]},
    package_dir={"atlassian": "atlassian"},
    include_package_data=True,

    zip_safe=False,
    install_requires=["requests==2.4.3"],

    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)

