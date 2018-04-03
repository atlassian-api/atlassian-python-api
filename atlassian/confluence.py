import logging, os
from requests.exceptions import HTTPError
from .rest_client import AtlassianRestAPI


log = logging.getLogger('atlassian.confluence')


class Confluence(AtlassianRestAPI):

    content_types = {
         ".gif": "image/gif",
         ".png": "image/png",
         ".jpg": "image/jpeg",
         ".jpeg": "image/jpeg",
         ".jpeg": "image/jpeg",
         ".pdf": "application/pdf",
    }

    def page_exists(self, space, title):
        try:
            self.get_page_by_title(space, title)
            log.info('Page "{title}" already exists in space "{space}"'.format(space=space, title=title))
            return True
        except (HTTPError, KeyError, IndexError):
            log.info('Page "{title}" does not exist in space "{space}"'.format(space=space, title=title))
            return False

    def get_page_id(self, space, title):
        return self.get_page_by_title(space, title).get('id')

    def get_page_space(self, page_id):
        return self.get_page_by_id(page_id, expand='space')['space']['key']

    def get_page_by_title(self, space, title):
        url = 'rest/api/content?spaceKey={space}&title={title}'.format(space=space, title=title)
        return self.get(url)['results'][0]

    def get_page_by_id(self, page_id, expand=None):
        url = 'rest/api/content/{page_id}?expand={expand}'.format(page_id=page_id, expand=expand)
        return self.get(url)

    def create_page(self, space, title, body, parent_id = None, type='page'):
        log.info('Creating {type} "{space}" -> "{title}"'.format(space=space, title=title, type=type))
        data={
            'type': type,
            'title': title,
            'space': {'key': space},
            'body': {'storage': {
                'value': body,
                'representation': 'storage'}}}
        if parent_id:
            data['ancestors'] = [{'type': type, 'id': parent_id}]
        return self.post('rest/api/content/', data = data)


    def attachFiles(self, files, page_id = None, title = None, space = None):
         """
         Attach (upload) file(s) to a page, if it exists it will update the
         automatically version the new file and keep the old ones.
         :param title: The page name
         :type  title: ``str``
         :param space: The space name
         :type  space: ``str``
         :param page_id: The page id to which we would like to upload the file
         :type  page_id: ``str``
         :param files: The files to upload
         :type  files: ``dict`` where `key` is filename and `value` is the comment.
         """
         page_id = self.get_page_id(space=space, title=title) if page_id is None else page_id
         type = 'attachment'
         if page_id is not None:
             for filename in files.keys():
                extension = os.path.splitext(filename)[-1]
                content_type = self.content_types.get(extension, "application/binary")
                data = {
                    'type': type,
                    "fileName": filename,
                    "contentType": content_type,
                    "comment": files[filename],
                    "minorEdit": "true"}
                headers = {
                    'X-Atlassian-Token': 'nocheck',
                    'Accept': 'application/json'}
                path = 'rest/api/content/{page_id}/child/attachment'.format(page_id=page_id)
                files = {'file': open(filename, 'rb')}
                # Check if there is already a file with the same name
                attachments = self.get(path=path, headers=headers, params = {'filename': filename} )
                if attachments['size']:
                    path = path + '/' + attachments['results'][0]['id'] + '/data'
                return self.post(path=path, data=data, headers=headers, files=files)
         else:
             log.warn("No 'page_id' found, not uploading attachments")

    def history(self, page_id):
        return self.get('rest/api/content/{0}/history'.format(page_id))

    def is_page_content_is_already_updated(self, page_id, body):
        confluence_content = self.get_page_by_id(page_id, expand='body.storage')['body']['storage']['value']
        confluence_content = confluence_content.replace('&oacute;', 'ó')

        log.debug('Old Content: """{body}"""'.format(body=confluence_content))
        log.debug('New Content: """{body}"""'.format(body=body))

        if confluence_content == body:
            log.warning('Content of {page_id} is exactly the same'.format(page_id=page_id))
            return True
        else:
            log.info('Content of {page_id} differs'.format(page_id=page_id))
            return False

    def update_page(self, parent_id, page_id, title, body, type='page'):
        log.info('Updating {type} "{title}"'.format(title=title, type=type))

        if self.is_page_content_is_already_updated(page_id, body):
            return self.get_page_by_id(page_id)
        else:
            version = self.history(page_id)['lastUpdated']['number'] + 1

            data = {
                'id': page_id,
                'type': type,
                'title': title,
                'body': {'storage': {
                    'value': body,
                    'representation': 'storage'}},
                'version': {'number': version}
            }

            if parent_id:
                data['ancestors'] = [{'type': 'page', 'id': parent_id}]

            return self.put('rest/api/content/{0}'.format(page_id), data=data)

    def update_or_create(self, parent_id, title, body):
        space = self.get_page_space(parent_id)

        if self.page_exists(space, title):
            page_id = self.get_page_id(space, title)
            result = self.update_page(parent_id, page_id, title, body)
        else:
            result = self.create_page(space, parent_id, title, body)

        log.warning('You may access your page at: {host}{url}'.format(
            host=self.url,
            url=result['_links']['tinyui']))

        return result

