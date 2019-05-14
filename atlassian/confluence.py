# coding: utf8
from .rest_client import AtlassianRestAPI
from requests import HTTPError
import logging
import os
import time

log = logging.getLogger(__name__)


class Confluence(AtlassianRestAPI):
    content_types = {
        ".gif": "image/gif",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".pdf": "application/pdf",
        ".doc": "application/msword",
        ".xls": "application/vnd.ms-excel",
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
            params['start'] = int(start)
        if limit is not None:
            params['limit'] = int(limit)

        url = 'rest/api/content/{page_id}/child/{type}'.format(page_id=page_id, type=type)
        log.info(url)
        try:
            return (self.get(url, params=params) or {}).get('results')
        except IndexError as e:
            log.error(e)
            return None

    def get_child_pages(self, page_id):
        """
        Get child pages for the provided page_id
        :param page_id:
        :return:
        """
        return self.get_page_child_by_type(page_id=page_id, type='page')

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
        url = 'rest/api/content'
        params = {}
        if start is not None:
            params['start'] = int(start)
        if limit is not None:
            params['limit'] = int(limit)
        if space is not None:
            params['spaceKey'] = str(space)
        if space is not None:
            params['title'] = str(title)
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
        url = 'rest/api/content/{id}/label'.format(id=page_id)
        params = {}
        if prefix:
            params['prefix'] = prefix
        if start is not None:
            params['start'] = int(start)
        if limit is not None:
            params['limit'] = int(limit)
        return self.get(url, params=params)

    def get_draft_page_by_id(self, page_id, status='draft'):
        """
        Provide content by id with status = draft
        :param page_id:
        :param status:
        :return:
        """
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
        url = 'rest/api/content/search'
        params = {}
        if label:
            params['cql'] = 'type={type}%20AND%20label={label}'.format(type='page',
                                                                       label=label)
        if start:
            params['start'] = start
        if limit:
            params['limit'] = limit
        return (self.get(url, params=params) or {}).get('results')

    def get_all_pages_from_space(self, space, start=0, limit=500, status=None):
        """
        Get all pages from space
        :param space:
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: The limit of the number of pages to return, this may be restricted by
                            fixed system limits. Default: 50
        :param status: OPTIONAL
        :return:
        """
        url = 'rest/api/content'
        params = {}
        if space:
            params['spaceKey'] = space
        if start:
            params['start'] = start
        if limit:
            params['limit'] = limit
        if status:
            params['status'] = status
        return (self.get(url, params=params) or {}).get('results')

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
        return self.get_all_pages_from_space(space, start, limit, status)

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
        return self.get_all_pages_from_space(space, start, limit, status)

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
        if limit:
            params['limit'] = limit
        if start:
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
        url = 'rest/api/content/{page_id}'.format(page_id=page_id)
        if recursive:
            children_pages = self.get_page_child_by_type(page_id)
            for children_page in children_pages:
                self.remove_page(children_page.get('id'), status, recursive)
        params = {}
        if status:
            params['status'] = status
        return self.delete(url, params=params)

    def create_page(self, space, title, body, parent_id=None, type='page',
                    representation='storage'):
        """
        Create page from scratch
        :param space:
        :param title:
        :param body:
        :param parent_id:
        :param type:
        :param representation: OPTIONAL: either Confluence 'storage' or 'wiki' markup format
        :return:
        """
        log.info('Creating {type} "{space}" -> "{title}"'.format(space=space, title=title, type=type))
        if representation not in ['wiki', 'storage']:
            raise ValueError("Wrong value for representation, it should be either wiki or storage")
        url = 'rest/api/content/'
        data = {
            'type': type,
            'title': title,
            'space': {'key': space},
            'body': {representation: {
                'value': body,
                'representation': representation}}}
        if parent_id:
            data['ancestors'] = [{'type': type, 'id': parent_id}]
        return self.post(url, data=data)

    def get_all_spaces(self, start=0, limit=500):
        """
        Get all spaces with provided limit
        :param start: OPTIONAL: The start point of the collection to return. Default: None (0).
        :param limit: OPTIONAL: The limit of the number of pages to return, this may be restricted by
                            fixed system limits. Default: 500
        """
        url = 'rest/api/space'
        params = {}
        if limit:
            params['limit'] = limit
        if start:
            params['start'] = start
        return (self.get(url, params=params) or {}).get('results')

    def add_comment(self, page_id, text):
        """
        Add comment into page
        :param page_id
        :param text
        """
        data = {'type': 'comment',
                'container': {'id': page_id, 'type': 'page', 'status': 'current'},
                'body': {'storage': {'value': text, 'representation': 'storage'}}}
        return self.post('rest/api/content/', data=data)

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
            # get base name of the file to get the attachment from confluence.
            file_base_name = os.path.basename(filename)
            # Check if there is already a file with the same name
            attachments = self.get(path=path, headers=headers, params={'filename': file_base_name})
            if attachments['size']:
                path = path + '/' + attachments['results'][0]['id'] + '/data'
            with open(filename, 'rb') as infile:
                return self.post(path=path, data=data, headers=headers,
                                 files={'file': (filename, infile, content_type)})
        else:
            log.warning("No 'page_id' found, not uploading attachments")
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
        url = 'rest/api/content/{0}/history'.format(page_id)
        return self.get(url)

    def get_content_history(self, content_id):
        return self.history(content_id)

    def get_content_history_by_version_number(self, content_id, version_number):
        url = 'rest/experimental/content/{0}/version/{1}'.format(content_id, version_number)
        return self.get(url)

    def remove_content_history(self, page_id, version_number):
        """
        Remove content history. It works as experimental method
        :param page_id:
        :param version_number: version number
        :return:
        """
        url = 'rest/experimental/content/{id}/version/{versionNumber}'.format(id=page_id, versionNumber=version_number)
        self.delete(url)

    def remove_content_history_in_cloud(self, page_id, version_id):
        """
        Remove content history. It works in CLOUD
        :param page_id:
        :param version_id:
        :return:
        """
        url = 'rest/api/content/{id}/version/{versionId}'.format(id=page_id, versionId=version_id)
        self.delete(url)

    def has_unknown_attachment_error(self, page_id):
        """
        Check has unknown attachment error on page
        :param page_id:
        :return:
        """
        unknown_attachment_identifier = 'plugins/servlet/confluence/placeholder/unknown-attachment'
        result = self.get_page_by_id(page_id, expand='body.view')
        if len(result) == 0:
            return ""
        body = (((result.get('body') or {}).get('view') or {}).get('value') or {})
        if unknown_attachment_identifier in body:
            return result.get('_links').get('base') + result.get('_links').get('tinyui')
        return ""

    def is_page_content_is_already_updated(self, page_id, body):
        """
        Compare content and check is already updated or not
        :param page_id: Content ID for retrieve storage value
        :param body: Body for compare it
        :return: True if the same
        """
        confluence_content = (self.get_page_by_id(page_id, expand='body.storage').get('body') or {}).get('storage').get(
            'value')
        confluence_content = confluence_content.replace('&oacute;', u'ó')

        log.debug('Old Content: """{body}"""'.format(body=confluence_content))
        log.debug('New Content: """{body}"""'.format(body=body))

        if confluence_content == body:
            log.warning('Content of {page_id} is exactly the same'.format(page_id=page_id))
            return True
        else:
            log.info('Content of {page_id} differs'.format(page_id=page_id))
            return False

    def update_page(self, parent_id, page_id, title, body, type='page',
                    minor_edit=False):
        """
        Update page if already exist
        :param parent_id:
        :param page_id:
        :param title:
        :param body:
        :param type:
        :param minor_edit: Indicates whether to notify watchers about changes.
            If False then notifications will be sent.
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
                'version': {'number': version,
                            'minorEdit': minor_edit}
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

        log.info('You may access your page at: {host}{url}'.format(host=self.url,
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
        headers = self.form_token_headers
        return self.delete('rest/cacheManagement/1.0/cacheEntries', headers=headers)

    def clean_package_cache(self, cache_name='com.gliffy.cache.gon'):
        """ Clean caches from cache management
            e.g.
            com.gliffy.cache.gon
            org.hibernate.cache.internal.StandardQueryCache_v5
        """
        headers = self.form_token_headers
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

    def create_space(self, space_key, space_name):
        """
        Create space
        :param space_key:
        :param space_name:
        :return:
        """
        data = {
            'key': space_key,
            'name': space_name
        }
        self.post('rest/api/space', data=data)

    def delete_space(self, space_key):
        """
        Delete space
        :param space_key:
        :return:
        """
        url = 'rest/api/space/{}'.format(space_key)
        return self.delete(url)

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

    def cql(self, cql, start=0, limit=None, expand=None, include_archived_spaces=None, excerpt=None):
        """
        Get results from cql search result with all related fields
        Search for entities in Confluence using the Confluence Query Language (CQL)
        :param cql:
        :param start: OPTIONAL: The start point of the collection to return. Default: 0.
        :param limit: OPTIONAL: The limit of the number of issues to return, this may be restricted by
                        fixed system limits. Default by built-in method: 25
        :param excerpt: the excerpt strategy to apply to the result, one of : indexed, highlight, none.
                        This defaults to highlight
        :param expand: OPTIONAL: the properties to expand on the search result,
                        this may cause database requests for some properties
        :param include_archived_spaces: OPTIONAL: whether to include content in archived spaces in the result,
                                    this defaults to false
        :return:
        """
        params = {}
        if start is not None:
            params['start'] = int(start)
        if limit is not None:
            params['limit'] = int(limit)
        if cql is not None:
            params['cql'] = cql
        if expand is not None:
            params['expand'] = expand
        if include_archived_spaces is not None:
            params['includeArchivedSpaces'] = include_archived_spaces
        if excerpt is not None:
            params['excerpt'] = excerpt

        return self.get('rest/api/search', params=params)

    def get_page_as_pdf(self, page_id):
        """
        Export page as standard pdf exporter
        :param page_id: Page ID
        :return: PDF File
        """
        headers = self.form_token_headers
        url = 'spaces/flyingpdf/pdfpageexport.action?pageId={pageId}'.format(pageId=page_id)
        if self.api_version == 'cloud':
            url = self.get_pdf_download_url_for_confluence_cloud(url)

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

    def health_check(self):
        """
        Get health status
        https://confluence.atlassian.com/jirakb/how-to-retrieve-health-check-results-using-rest-api-867195158.html
        :return:
        """
        # check as Troubleshooting & Support Tools Plugin
        response = self.get('rest/troubleshooting/1.0/check/')
        if not response:
            # check as support tools
            response = self.get('rest/supportHealthCheck/1.0/check/')
        return response

    def get_pdf_download_url_for_confluence_cloud(self, url):
        """
        Confluence cloud does not return the PDF document when the PDF
        export is initiated. Instead it starts a process in the background 
        and provides a link to download the PDF once the process completes.
        This functions polls the long running task page and returns the
        download url of the PDF.
        :param url: URL to initiate PDF export
        :return: Download url for PDF file
        """
        download_url = None
        try:
            long_running_task = True
            headers = self.form_token_headers
            log.info('Initiate PDF export from Confluence Cloud')
            response = self.get(url, headers=headers, not_json_response=True)
            response_string = response.decode(encoding='utf-8', errors='strict')
            task_id = response_string.split('name="ajs-taskId" content="')[1].split('">')[0]
            poll_url = 'runningtaskxml.action?taskId={0}'.format(task_id)
            while long_running_task:
                long_running_task_response = self.get(poll_url, headers=headers, not_json_response=True)
                long_running_task_response_parts = long_running_task_response.decode(encoding='utf-8',
                                                                                     errors='strict').split('\n')
                percentage_complete = long_running_task_response_parts[6].strip()
                is_successful = long_running_task_response_parts[7].strip()
                is_complete = long_running_task_response_parts[8].strip()
                log.info('Sleep for 5s.')
                time.sleep(5)
                log.info('Check if export task has completed.')
                if is_complete == '<isComplete>true</isComplete>':
                    if is_successful == '<isSuccessful>true</isSuccessful>':
                        log.info(percentage_complete)
                        log.info('Downloading content...')
                        log.debug('Extract taskId and download PDF.')
                        current_status = long_running_task_response_parts[3]
                        download_url = current_status.split('href=&quot;/wiki/')[1].split('&quot')[0]
                        long_running_task = False
                    elif is_successful == '<isSuccessful>false</isSuccessful>':
                        log.error('PDF conversion not successful.')
                        return None
                else:
                    log.info(percentage_complete)
        except IndexError as e:
            log.error(e)
            return None

        return download_url
