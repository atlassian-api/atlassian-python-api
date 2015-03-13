import logging
from atlassian import AtlassianRestAPI


log = logging.getLogger('atlassian.confluence')


class Confluence(AtlassianRestAPI):

    def create_page(self, space, parent_id, title, body):
        return self.post('/rest/api/content/', data={
            'type': 'page',
            'ancestors': [{'type': 'page', 'id': parent_id}],
            'title': title,
            'space': {'key': space},
            'body': {'storage': {
                'value': body,
                'representation': 'storage'}}})

    def history(self, page_id):
        return self.get('/rest/api/content/{0}/history'.format(page_id))

    def update_page(self, parent_id, page_id, title, body, type='page',):
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
