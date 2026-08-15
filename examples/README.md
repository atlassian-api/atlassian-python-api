# Examples and apps

Here you can find different examples of how to use a library.

You can use it as a reference for your apps or just use it "as is" for your needs.
Feel free to send us new examples if you think, that we miss something important.

For Bitbucket Cloud's object-oriented client, see
`bitbucket/bitbucket_cloud_read_source.py` for reading a repository file and
browsing a directory without using the legacy Bitbucket Server API.

For Bitbucket Server/Data Center pagination, see
`bitbucket/bitbucket_server_project_open_pull_requests.py`. Methods that list
projects, repositories, or pull requests return generators: use them directly
in a `for` loop, or call `list(...)` only for small result sets.

For a Server/Data Center release report that lists merged pull requests between
two tags or commits, see `bitbucket/bitbucket_server_release_report.py`.

There are simple rules each example should follow:

* **Do not store** any credentials in VCS
* Do not use any additional dependencies except the python build-in's
* Follow the PEP-8 and format your code.

JetBrains PyCharm built-in formatter is perfectly fine and used a lot at this library
