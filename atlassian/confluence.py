import logging
from requests.exceptions import HTTPError
from atlassian import AtlassianRestAPI


log = logging.getLogger('atlassian.confluence')


class Confluence(AtlassianRestAPI):

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
        url = '/rest/api/content?spaceKey={space}&title={title}'.format(space=space, title=title)
        return self.get(url)['results'][0]

    def get_page_by_id(self, page_id, expand=None):
        url = '/rest/api/content/{page_id}?expand={expand}'.format(page_id=page_id, expand=expand)
        return self.get(url)

    def create_page(self, space, parent_id, title, body, type='page'):
        log.info('Creating {type} "{space}" -> "{title}"'.format(space=space, title=title, type=type))
        return self.post('/rest/api/content/', data={
            'type': type,
            'ancestors': [{'type': type, 'id': parent_id}],
            'title': title,
            'space': {'key': space},
            'body': {'storage': {
                'value': body,
                'representation': 'storage'}}})

    def history(self, page_id):
        return self.get('/rest/api/content/{0}/history'.format(page_id))

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
            return self.put('/rest/api/content/{0}'.format(page_id), data={
                'id': page_id,
                'type': type,
                'ancestors': [{'type': 'page', 'id': parent_id}],
                'title': title,
                'body': {'storage': {
                    'value': body,
                    'representation': 'storage'}},
                'version': {'number': version}})

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
