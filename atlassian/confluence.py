# coding: utf8
from .rest_client import AtlassianRestAPI
from requests import HTTPError
import logging
import os

log = logging.getLogger(__name__)


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
            if self.get_page_by_title(space, title):
                log.info('Page "{title}" already exists in space "{space}"'.format(space=space, title=title))
                return True
            else:
                log.info('Page does not exist because did not find by title search')
                return False
        except (HTTPError, KeyError, IndexError):
            log.info('Page "{title}" does not exist in space "{space}"'.format(space=space, title=title))
            return False

    def get_page_child_by_type(self, page_id, type='page', start=None, limit=None):
        """
        Provide content by type (page, blog, comment)
        :param page_id: A string containing the id of the type content container.
        :param type:
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: how many items should be returned after the start index. Default: Site limit 200.
        :return:
        """
        params = {}
        if start is not None:
            params["start"] = int(start)
        if limit is not None:
            params["limit"] = int(limit)

        url = 'rest/api/content/{page_id}/child/{type}'.format(page_id=page_id, type=type)
        log.info(url)
        try:
            return (self.get(url, params=params) or {}).get('results')
        except IndexError as e:
            log.error(e)
            return None

    def get_page_id(self, space, title):
        """
        Provide content id from search result by title and space
        :param space: SPACE key
        :param title: title
        :return:
        """
        return (self.get_page_by_title(space, title) or {}).get('id')

    def get_page_space(self, page_id):
        """
        Provide space key from content id
        :param page_id: content ID
        :return:
        """
        return ((self.get_page_by_id(page_id, expand='space') or {}).get('space') or {}).get('key')

    def get_page_by_title(self, space, title, start=None, limit=None):
        """
        Returns the list of labels on a piece of Content.
        :param space: Space key
        :param title: Title of the page
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: The limit of the number of labels to return, this may be restricted by
                            fixed system limits. Default: 200.
        :return: The JSON data returned from searched results the content endpoint, or the results of the
                 callback. Will raise requests.HTTPError on bad input, potentially.
                 If it has IndexError then return the None.
        """
        params = {}
        if start is not None:
            params["start"] = int(start)
        if limit is not None:
            params["limit"] = int(limit)
        if space is not None:
            params['spaceKey'] = str(space)
        if space is not None:
            params['title'] = str(title)
        url = 'rest/api/content'
        try:
            return (self.get(url, params=params) or {}).get('results')[0]
        except IndexError as e:
            log.error(e)
            return None

    def get_page_by_id(self, page_id, expand=None):
        """
        Get page by ID
        :param page_id: Content ID
        :param expand: OPTIONAL: expand e.g. history
        :return:
        """
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
        return (self.get(url) or {}).get('results')

    def get_all_pages_from_space(self, space, start=0, limit=500):
        """
        Get all pages from space
        :param space:
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: The limit of the number of pages to return, this may be restricted by
                            fixed system limits. Default: 50
        :return:
        """
        url = 'rest/api/content?spaceKey={space}&limit={limit}&start={start}'.format(space=space,
                                                                                     limit=limit,
                                                                                     start=start)
        return (self.get(url) or {}).get('results')

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
        return (self.get(url) or {}).get('results')

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
        return (self.get(url) or {}).get('results')

    def get_all_draft_pages_from_space_through_cql(self, space, start=0, limit=500, status='draft'):
        """
        Search list of draft pages by space key
        Use case is cleanup old drafts from Confluence
        :param space: Space Key
        :param status: Can be changed
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: The limit of the number of pages to return, this may be restricted by
                            fixed system limits. Default: 500
        :return:
        """
        url = 'rest/api/content?cql=space=spaceKey={space} and status={status}'.format(space=space,
                                                                                       status=status)
        params = {}
        params['limit'] = limit
        params['start'] = start
        return (self.get(url, params=params) or {}).get('results')

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
        This method removes a page from trash
        :param page_id:
        :return:
        """
        return self.remove_page(page_id=page_id, status='trashed')

    def remove_page_as_draft(self, page_id):
        """
        This method removes a page from trash if it is a draft
        :param page_id:
        :return:
        """
        return self.remove_page(page_id=page_id, status='draft')

    def remove_page(self, page_id, status=None, recursive=False):
        """
        This method removes a page, if it has recursive flag, method removes including child pages
        :param page_id:
        :param status: OPTIONAL: type of page
        :param recursive: OPTIONAL: if True - will recursively delete all children pages too
        :return:
        """
        if recursive:
            children_pages = self.get_page_child_by_type(page_id)
            for children_page in children_pages:
                self.remove_page(children_page.get('id'), status, recursive)
        if status is None:
            url = 'rest/api/content/{page_id}'.format(page_id=page_id)
        else:
            url = 'rest/api/content/{page_id}?status={status}'.format(page_id=page_id, status=status)

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
        return (self.get(url) or {}).get('results')

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

    def set_page_label(self, page_id, label):
        """
        Set a label on the page
        :param page_id: content_id format
        :param label: label to add
        :return:
        """
        url = 'rest/api/content/{page_id}/label'.format(page_id=page_id)
        data = {'prefix': 'global',
                'name': label}
        return self.post(path=url, data=data)

    def history(self, page_id):
        return self.get('rest/api/content/{0}/history'.format(page_id))

    def is_page_content_is_already_updated(self, page_id, body):
        """
        Compare content and check is already updated or not
        :param page_id: Content ID for retrieve storage value
        :param body: Body for compare it
        :return: True if the same
        """
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
        Update page or create a page if it is not exists
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

    def convert_storage_to_view(self, storage):
        """
        Convert from Confluence XHTML format to view format
        :param storage:
        :return:
        """
        data = {'value': storage,
                'representation': 'storage'}
        return self.post('rest/api/contentbody/convert/view', data=data)

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

    def get_page_ancestors(self, page_id):
        """
        Provide the ancestors from the page (content) id
        :param page_id: content_id format
        :return: get properties
        """
        url = 'rest/api/content/{page_id}?expand=ancestors'.format(page_id=page_id)
        return (self.get(path=url) or {}).get('ancestors')

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

        return (self.get(url) or {}).get('results')

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
        return (self.get(url) or {}).get('results')

    def get_space(self, space_key, expand='description.plain,homepage'):
        """
        Get information about a space through space key
        :param space_key: The unique space key name
        :param expand: OPTIONAL: additional info from description, homepage
        :return: Returns the space along with its ID
        """
        url = 'rest/api/space/{space_key}?expand={expand}'.format(space_key=space_key,
                                                                  expand=expand)
        return self.get(url)

    def get_user_details_by_username(self, username, expand=None):
        """
        Get information about a user through username
        :param username: The user name
        :param expand: OPTIONAL expand for get status of user.
                Possible param is "status". Results are "Active, Deactivated"
        :return: Returns the user details
        """
        if expand:
            url = 'rest/api/user?username={username}&expand={expand}'.format(username=username,
                                                                             expand=expand)
        else:
            url = 'rest/api/user?username={username}'.format(username=username)

        return self.get(url)

    def get_user_details_by_userkey(self, userkey, expand=None):
        """
        Get information about a user through user key
        :param userkey: The user key
        :param expand: OPTIONAL expand for get status of user.
                Possible param is "status". Results are "Active, Deactivated"
        :return: Returns the user details
        """
        if expand:
            url = 'rest/api/user?key={userkey}&expand={expand}'.format(userkey=userkey,
                                                                       expand=expand)
        else:
            url = 'rest/api/user?key={userkey}'.format(userkey=userkey)
        return self.get(url)

    def cql(self, cql, start=0, limit=None):
        """
        Get results from cql search result with all related fields
        :param cql:
        :param start: OPTIONAL: The start point of the collection to return. Default: 0.
        :param limit: OPTIONAL: The limit of the number of issues to return, this may be restricted by
                fixed system limits. Default by built-in method: 25
        :return:
        """
        params = {}
        if start is not None:
            params["start"] = int(start)
        if limit is not None:
            params["limit"] = int(limit)
        if cql is not None:
            params['cql'] = cql
        return self.get('rest/api/search', params=params)

    def get_page_as_pdf(self, page_id):
        """
        Export page as standard pdf exporter
        :param page_id: Page ID
        :return: PDF File
        """
        headers = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Atlassian-Token': 'no-check'}
        url = 'spaces/flyingpdf/pdfpageexport.action?pageId={pageId}'.format(pageId=page_id)
        return self.get(url, headers=headers, not_json_response=True)

    def export_page(self, page_id):
        """
        Alias method for export page as pdf
        :param page_id: Page ID
        :return: PDF File
        """
        return self.get_page_as_pdf(page_id)

    def get_descendant_page_id(self, space, parent_id, title):
        """
        Provide  space, parent_id and title of the descendant page, it will return the descendant page_id
        :param space: str
        :param parent_id: int
        :param title: str
        :return: page_id of the page whose title is passed in argument
        """
        page_id = ""

        url = 'rest/api/content/search?cql=parent={}%20AND%20space="{}"'.format(
            parent_id, space
        )
        response = self.get(url, {})

        for each_page in response.get("results", []):
            if each_page.get("title") == title:
                page_id = each_page.get("id")
                break
        return page_id

    def reindex(self):
        """
        It is not public method for reindex Confluence
        :return:
        """
        url = 'rest/prototype/1/index/reindex'
        return self.post(url)

    def reindex_get_status(self):
        """
        Get reindex status of Confluence
        :return:
        """
        url = 'rest/prototype/1/index/reindex'
        return self.get(url)
