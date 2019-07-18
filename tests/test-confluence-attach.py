import tempfile
import json
import os
import unittest
from atlassian import Confluence


class TestConfluenceAuth(unittest.TestCase):

    def test_confluence_auth(self):
        credentials = None
        secret_file = '../credentials.secret'

        '''
            Keep the credentials private, the file is excluded. There is an example for credentials.secret
            See also: http://www.blacktechdiva.com/hide-api-keys/
            
            {
              "host" : "https://localhost:8080",
              "username" : "john_doe",
              "password" : "12345678"
            }        
        '''

        try:
            with open(secret_file) as json_file:
                credentials = json.load(json_file)
        except Exception as err:
            self.fail('[{0}]: {1}'.format(secret_file, err))

        confluence = Confluence(
            url=credentials['host'],
            username=credentials['username'],
            password=credentials['password'])

        # individual configuration
        space = 'SAN'
        title = 'atlassian-python-rest-api-wrapper'

        # TODO: check if page are exists

        fd, filename = tempfile.mkstemp('w')
        os.write(fd, b'Hello World - Version 1')

        # upload a new file
        result = confluence.attach_file(filename, None, title=title, space=space, comment='upload from unittest')

        # attach_file() returns: {'results': [{'id': 'att144005326', 'type': 'attachment', ...
        self.assertTrue('results' in result)
        self.assertFalse('statusCode' in result)

        # upload a new version of an existing file
        os.write(fd, b'Hello Universe - Version 2')
        result = confluence.attach_file(filename, None, title=title, space=space, comment='upload from unittest')

        # attach_file() returns: {'id': 'att144005326', 'type': 'attachment', ...
        self.assertTrue('id' in result)
        self.assertFalse('statusCode' in result)

        os.close(fd)
        os.remove(filename)


if __name__ == '__main__':
    unittest.main()
