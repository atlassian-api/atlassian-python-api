# coding: utf8
import logging
import re

log = logging.getLogger(__name__)


def is_email(string):
    """
    >>> is_email('username@example.com')
    True
    >>> is_email('example.com')
    False
    >>> is_email('firstname.lastname@domain.co.uk')
    True
    """
    email_regex = r'^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$'

    if isinstance(string, str) and not re.match(email_regex, string):
        return False
    else:
        return True


def html_email(email, title=None):
    """
    >>> html_email('username@example.com')
    '<a href="mailto:username@example.com">username@example.com</a>'
    """

    if not title:
        title = email

    return '<a href="mailto:{email}">{title}</a>'.format(email=email, title=title)


def html_list(data):
    """
    >>> html_list(['example.com', 'admin1@example.com', 'admin2@example.com'])
    '<ul><li>example.com</li><li><a href="mailto:admin1@example.com">admin1@example.com</a></li><li><a href="mailto:admin2@example.com">admin2@example.com</a></li></ul>'
    """
    html = '<ul>'

    for item in data:

        if isinstance(item, dict):
            if item.get('email'):
                item = html_email(item.get('email'), item.get('name', None))
            elif item.get('name'):
                item = item.get('name')

        if is_email(item):
            item = html_email(item, item)

        html += '<li>{}</li>'.format(item)

    return html + '</ul>'


def html_table_header_row(data):
    """
    >>> html_table_header_row(['administrators', 'key', 'leader', 'project'])
    '\\n\\t<tr><th>Administrators</th><th>Key</th><th>Leader</th><th>Project</th></tr>'
    >>> html_table_header_row(['key', 'project', 'leader', 'administrators'])
    '\\n\\t<tr><th>Key</th><th>Project</th><th>Leader</th><th>Administrators</th></tr>'
    """
    html = '\n\t<tr>'

    for th in data:
        title = th.replace('_', ' ').title()
        html += '<th>{}</th>'.format(title)

    return html + '</tr>'


def html_row_with_ordered_headers(data, headers):
    """
    >>> headers = ['administrators', 'key', 'leader', 'project']
    >>> data = {'key': 'DEMO', 'project': 'Demonstration', 'leader': 'leader@example.com', 'administrators': ['admin1@example.com', 'admin2@example.com']}
    >>> html_row_with_ordered_headers(data, headers)
    '\\n\\t<tr><td><ul><li><a href="mailto:admin1@example.com">admin1@example.com</a></li><li><a href="mailto:admin2@example.com">admin2@example.com</a></li></ul></td><td>DEMO</td><td>leader@example.com</td><td>Demonstration</td></tr>'
    >>> headers = ['key', 'project', 'leader', 'administrators']
    >>> html_row_with_ordered_headers(data, headers)
    '\\n\\t<tr><td>DEMO</td><td>Demonstration</td><td>leader@example.com</td><td><ul><li><a href="mailto:admin1@example.com">admin1@example.com</a></li><li><a href="mailto:admin2@example.com">admin2@example.com</a></li></ul></td></tr>'
    """
    html = '\n\t<tr>'

    for header in headers:
        element = data[header]

        if isinstance(element, list):
            element = html_list(element)

        if is_email(element):
            element = html_email(element)

        html += '<td>{}</td>'.format(element)

    return html + '</tr>'


def html_table_from_dict(data, ordering):
    """
    >>> ordering = ['administrators', 'key', 'leader', 'project']
    >>> data = [ \
        {'key': 'DEMO', 'project': 'Demonstration', 'leader': 'leader@example.com', 'administrators': ['admin1@example.com', 'admin2@example.com']}, \
        {'key': 'FOO', 'project': 'Foo', 'leader': 'foo@example.com', 'administrators': ['foo-admin1@example.com', 'foo-admin2@example.com']}, \
        {'key': 'BAR', 'project': 'Bar', 'leader': 'bar@example.com', 'administrators': ['bar-admin1@example.com', 'bar-admin2@example.com']}]
    >>> html_table_from_dict(data, ordering)
    '<table><tbody>\\n<tr><th>Administrators</th><th>Key</th><th>Leader</th><th>Project</th></tr>\\n<tr><td><ul><li><a href="mailto:admin1@example.com">admin1@example.com</a></li><li><a href="mailto:admin2@example.com">admin2@example.com</a></li></ul></td><td>DEMO</td><td>leader@example.com</td><td>Demonstration</td></tr>\\n<tr><td><ul><li><a href="mailto:foo-admin1@example.com">foo-admin1@example.com</a></li><li><a href="mailto:foo-admin2@example.com">foo-admin2@example.com</a></li></ul></td><td>FOO</td><td>foo@example.com</td><td>Foo</td></tr>\\n<tr><td><ul><li><a href="mailto:bar-admin1@example.com">bar-admin1@example.com</a></li><li><a href="mailto:bar-admin2@example.com">bar-admin2@example.com</a></li></ul></td><td>BAR</td><td>bar@example.com</td><td>Bar</td></tr>\\n</tbody></table>'
    >>> ordering = ['key', 'project', 'leader', 'administrators']
    >>> html_table_from_dict(data, ordering)
    '<table><tbody>\\n<tr><th>Key</th><th>Project</th><th>Leader</th><th>Administrators</th></tr>\\n<tr><td>DEMO</td><td>Demonstration</td><td>leader@example.com</td><td><ul><li><a href="mailto:admin1@example.com">admin1@example.com</a></li><li><a href="mailto:admin2@example.com">admin2@example.com</a></li></ul></td></tr>\\n<tr><td>FOO</td><td>Foo</td><td>foo@example.com</td><td><ul><li><a href="mailto:foo-admin1@example.com">foo-admin1@example.com</a></li><li><a href="mailto:foo-admin2@example.com">foo-admin2@example.com</a></li></ul></td></tr>\\n<tr><td>BAR</td><td>Bar</td><td>bar@example.com</td><td><ul><li><a href="mailto:bar-admin1@example.com">bar-admin1@example.com</a></li><li><a href="mailto:bar-admin2@example.com">bar-admin2@example.com</a></li></ul></td></tr>\\n</tbody></table>'
    """
    html = '<table><tbody>'
    html += html_table_header_row(ordering)

    for row in data:
        html += html_row_with_ordered_headers(row, ordering)

    return html + '\n</tbody></table>'
