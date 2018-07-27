# coding: utf8
from .rest_client import AtlassianRestAPI
from requests import HTTPError
import logging
import os

log = logging.getLogger('atlassian.confluence')


class Confluence(AtlassianRestAPI):
    content_types = {
        ".gif": "image/gif",
        ".png": "image/png",
        ".jpg": "image/jpeg",
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

    def get_page_labels(self, page_id, prefix=None, start=None, limit=None):
        """
        Returns the list of labels on a piece of Content.
        :param page_id: A string containing the id of the labels content container.
        :param prefix: OPTIONAL: The prefixes to filter the labels with {@see Label.Prefix}.
                                Default: None.
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: The limit of the number of labels to return, this may be restricted by
                            fixed system limits. Default: 200.
        :return: The JSON data returned from the content/{id}/label endpoint, or the results of the
                 callback. Will raise requests.HTTPError on bad input, potentially.
        """
        params = {}
        if prefix:
            params["prefix"] = prefix
        if start is not None:
            params["start"] = int(start)
        if limit is not None:
            params["limit"] = int(limit)
        return self.get("rest/api/content/{id}/label".format(id=page_id), params=params)

    def get_draft_page_by_id(self, page_id, status='draft'):
        url = 'rest/api/content/{page_id}?status={status}'.format(page_id=page_id, status=status)
        return self.get(url)

    def get_all_pages_by_label(self, label, start=0, limit=50):
        """
        Get all page by label
        :param label:
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: The limit of the number of pages to return, this may be restricted by
                      fixed system limits. Default: 50
        :return:
        """
        url = 'rest/api/content/search?cql=type={type}%20AND%20label={label}&limit={limit}&start={start}'.format(
            type='page',
            label=label,
            start=start,
            limit=limit)
        return self.get(url)

    def get_all_pages_from_space(self, space, start=0, limit=500):
        """
        Get all pages from Space
        :param space:
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: The limit of the number of pages to return, this may be restricted by
                            fixed system limits. Default: 50
        :return:
        """
        url = 'rest/api/content?spaceKey={space}&limit={limit}&start={start}'.format(space=space,
                                                                                     limit=limit,
                                                                                     start=start)
        return self.get(url)['results']

    def get_all_pages_from_space_trash(self, space, start=0, limit=500, status='trashed'):
        """
        Get list of pages from trash
        :param space:
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: The limit of the number of pages to return, this may be restricted by
                            fixed system limits. Default: 500
        :param status:
        :return:
        """
        url = 'rest/api/content?spaceKey={space}&limit={limit}&start={start}&status={status}'.format(space=space,
                                                                                                     limit=limit,
                                                                                                     start=start,
                                                                                                     status=status)
        return self.get(url)['results']

    def get_all_draft_pages_from_space(self, space, start=0, limit=500, status='draft'):
        """
        Get list of draft pages from space
        Use case is cleanup old drafts from Confluence
        :param space:
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: The limit of the number of pages to return, this may be restricted by
                            fixed system limits. Default: 500
        :param status:
        :return:
        """
        url = 'rest/api/content?spaceKey={space}&limit={limit}&start={start}&status={status}'.format(space=space,
                                                                                                     limit=limit,
                                                                                                     start=start,
                                                                                                     status=status)
        return self.get(url)['results']

    def get_all_restictions_for_content(self, content_id):
        """
        Returns info about all restrictions by operation.
        :param content_id:
        :return: Return the raw json response
        """
        url = 'rest/api/content/{}/restriction/byOperation'.format(content_id)
        return self.get(url)

    def remove_page_from_trash(self, page_id):
        """
        This method removed page from trash
        :param page_id:
        :return:
        """
        url = 'rest/api/content/{page_id}?status=trashed'.format(page_id=page_id)
        return self.delete(url)

    def remove_page(self, page_id):
        """
        This method removed page
        :param page_id:
        :return:
        """
        url = 'rest/api/content/{page_id}'.format(page_id=page_id)
        return self.delete(url)

    def create_page(self, space, title, body, parent_id=None, type='page'):
        """
        Create page from scratch
        :param space:
        :param title:
        :param body:
        :param parent_id:
        :param type:
        :return:
        """
        log.info('Creating {type} "{space}" -> "{title}"'.format(space=space, title=title, type=type))
        data = {
            'type': type,
            'title': title,
            'space': {'key': space},
            'body': {'storage': {
                'value': body,
                'representation': 'storage'}}}
        if parent_id:
            data['ancestors'] = [{'type': type, 'id': parent_id}]
        return self.post('rest/api/content/', data=data)

    def get_all_spaces(self, start=0, limit=500):
        """
        Get all spaces with provided limit
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: The limit of the number of pages to return, this may be restricted by
                            fixed system limits. Default: 500
        """
        url = 'rest/api/space?limit={limit}&start={start}'.format(limit=limit, start=start)
        return self.get(url)['results']

    def attach_file(self, filename, page_id=None, title=None, space=None, comment=None):
        """
        Attach (upload) a file to a page, if it exists it will update the
        automatically version the new file and keep the old one.
        :param title: The page name
        :type  title: ``str``
        :param space: The space name
        :type  space: ``str``
        :param page_id: The page id to which we would like to upload the file
        :type  page_id: ``str``
        :param filename: The file to upload
        :type  filename: ``str``
        :param comment: A comment describing this upload/file
        :type  comment: ``str``
        """
        page_id = self.get_page_id(space=space, title=title) if page_id is None else page_id
        type = 'attachment'
        if page_id is not None:
            extension = os.path.splitext(filename)[-1]
            content_type = self.content_types.get(extension, "application/binary")
            comment = comment if comment else "Uploaded {filename}.".format(filename=filename)
            data = {
                'type': type,
                "fileName": filename,
                "contentType": content_type,
                "comment": comment,
                "minorEdit": "true"}
            headers = {
                'X-Atlassian-Token': 'nocheck',
                'Accept': 'application/json'}
            path = 'rest/api/content/{page_id}/child/attachment'.format(page_id=page_id)
            # Check if there is already a file with the same name
            attachments = self.get(path=path, headers=headers, params={'filename': filename})
            if attachments['size']:
                path = path + '/' + attachments['results'][0]['id'] + '/data'
            with open(filename, 'rb') as infile:
                return self.post(path=path, data=data, headers=headers, files={'file': infile})
        else:
            log.warn("No 'page_id' found, not uploading attachments")
            return None

    def history(self, page_id):
        return self.get('rest/api/content/{0}/history'.format(page_id))

    def is_page_content_is_already_updated(self, page_id, body):
        confluence_content = self.get_page_by_id(page_id, expand='body.storage')['body']['storage']['value']
        confluence_content = confluence_content.replace('&oacute;', u'ó')

        log.debug('Old Content: """{body}"""'.format(body=confluence_content))
        log.debug('New Content: """{body}"""'.format(body=body))

        if confluence_content == body:
            log.warning('Content of {page_id} is exactly the same'.format(page_id=page_id))
            return True
        else:
            log.info('Content of {page_id} differs'.format(page_id=page_id))
            return False

    def update_page(self, parent_id, page_id, title, body, type='page'):
        """
        Update page if already exist
        :param parent_id:
        :param page_id:
        :param title:
        :param body:
        :param type:
        :return:
        """
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
        """
        Update page or create page if it is not exists
        :param parent_id:
        :param title:
        :param body:
        :return:
        """
        space = self.get_page_space(parent_id)

        if self.page_exists(space, title):
            page_id = self.get_page_id(space, title)
            result = self.update_page(parent_id=parent_id, page_id=page_id, title=title, body=body)
        else:
            result = self.create_page(space=space, parent_id=parent_id, title=title, body=body)

        log.warning('You may access your page at: {host}{url}'.format(
            host=self.url,
            url=result['_links']['tinyui']))

        return result

    def convert_wiki_to_storage(self, wiki):
        """
        Convert to Confluence XHTML format from wiki style
        :param wiki:
        :return:
        """
        data = {'value': wiki,
                'representation': 'wiki'}
        return self.post('rest/api/contentbody/convert/storage', data=data)

    def set_page_property(self, page_id, data):
        """
        Set the page (content) property e.g. add hash parameters
        :param page_id: content_id format
        :param data: data should be as json data
        :return:
        """
        url = 'rest/api/content/{page_id}/property'.format(page_id=page_id)
        json_data = data
        return self.post(path=url, data=json_data)

    def delete_page_property(self, page_id, page_property):
        """
        Delete the page (content) property e.g. delete key of hash
        :param page_id: content_id format
        :param page_property: key of property
        :return:
        """
        url = 'rest/api/content/{page_id}/property/{page_property}'.format(page_id=page_id,
                                                                           page_property=str(page_property))
        return self.delete(path=url)

    def get_page_property(self, page_id, page_property_key):
        """
        Get the page (content) property e.g. get key of hash
        :param page_id: content_id format
        :param page_property_key: key of property
        :return:
        """
        url = 'rest/api/content/{page_id}/property/{key}'.format(page_id=page_id,
                                                                 key=str(page_property_key))
        return self.get(path=url)

    def get_page_properties(self, page_id):
        """
        Get the page (content) properties
        :param page_id: content_id format
        :return: get properties
        """
        url = 'rest/api/content/{page_id}/property'.format(page_id=page_id)
        return self.get(path=url)

    def clean_all_caches(self):
        """ Clean all caches from cache management"""
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Atlassian-Token': 'no-check'}
        return self.delete('rest/cacheManagement/1.0/cacheEntries', headers=headers)

    def clean_package_cache(self, cache_name='com.gliffy.cache.gon'):
        """ Clean caches from cache management
            e.g.
            com.gliffy.cache.gon
            org.hibernate.cache.internal.StandardQueryCache_v5
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Atlassian-Token': 'no-check'}
        data = {'cacheName': cache_name}
        return self.delete('rest/cacheManagement/1.0/cacheEntries', data=data, headers=headers)

    def get_all_groups(self, start=0, limit=1000):
        """
        Get all groups from Confluence User management
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: The limit of the number of groups to return, this may be restricted by
                                fixed system limits. Default: 1000
        :return:
        """
        url = 'rest/api/group?limit={limit}&start={start}'.format(limit=limit,
                                                                  start=start)

        return self.get(url)['results']

    def get_group_members(self, group_name='confluence-users', start=0, limit=1000):
        """
        Get a paginated collection of users in the given group
        :param group_name
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: The limit of the number of users to return, this may be restricted by
                            fixed system limits. Default: 1000
        :return:
        """
        url = 'rest/api/group/{group_name}/member?limit={limit}&start={start}'.format(group_name=group_name,
                                                                                      limit=limit,
                                                                                      start=start)
        return self.get(url)['results']
