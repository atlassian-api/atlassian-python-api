# coding=utf-8
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
    '<ul>
        <li>example.com</li>
        <li><a href="mailto:admin1@example.com">admin1@example.com</a></li>
        <li><a href="mailto:admin2@example.com">admin2@example.com</a></li>
    </ul>'
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
        {'key': 'DEMO', 'project': 'Demo project', 'leader': 'lead@example.com', \
            'administrators': ['admin@example.com', 'root@example.com']},]
    >>> html_table_from_dict(data, ordering)
    '<table>
        <tbody>\\n
            <tr>
                <th>Administrators</th>
                <th>Key</th>
                <th>Leader</th>
                <th>Project</th>
            </tr>\\n
        <tr>
            <td>
                <ul>
                    <li><a href="mailto:admin@example.com">admin@example.com</a></li>
                    <li><a href="mailto:root@example.com">root@example.com</a></li>
                </ul>
            </td>
            <td>DEMO</td>
            <td>lead@example.com</td>
            <td>Demo project</td>
        </tr>\\n
        </tbody>
    </table>'
    >>> ordering = ['key', 'project', 'leader', 'administrators']
    >>> html_table_from_dict(data, ordering)
    '<table>
        <tbody>\\n
            <tr>
                <th>Key</th>
                <th>Project</th>
                <th>Leader</th>
                <th>Administrators</th>
            </tr>\\n
            <tr>
                <td>DEMO</td>
                <td>Demo project</td>
                <td>lead@example.com</td>
                <td>
                    <ul>
                        <li><a href="mailto:admin@example.com">admin@example.com</a></li>
                        <li><a href="mailto:root@example.com">root@example.com</a></li>
                    </ul>
                </td>
            </tr>\\n
        </tbody>
    </table>'
    """
    html = '<table><tbody>'
    html += html_table_header_row(ordering)

    for row in data:
        html += html_row_with_ordered_headers(row, ordering)

    return html + '\n</tbody></table>'


def block_code_macro_confluence(code, lang=None):
    """
    Wrap into code block macro
    :param code:
    :param lang:
    :return:
    """
    if not lang:
        lang = ''
    return ('''\
                <ac:structured-macro ac:name="code" ac:schema-version="1">
                    <ac:parameter ac:name="language">{lang}</ac:parameter>
                    <ac:plain-text-body><![CDATA[{code}]]></ac:plain-text-body>
                </ac:structured-macro>
            ''').format(lang=lang, code=code)


def html_code__macro_confluence(text):
    """
    Wrap into html macro
    :param text:
    :return:
    """
    return ('''\
                <ac:structured-macro ac:name="html" ac:schema-version="1">
                    <ac:plain-text-body><![CDATA[{text}]]></ac:plain-text-body>
                </ac:structured-macro>
            ''').format(text=text)


def noformat_code_macro_confluence(text, nopanel=None):
    """
    Wrap into code block macro
    :param text:
    :param nopanel: (bool) True or False Removes the panel around the content.
    :return:
    """
    if not nopanel:
        nopanel = False
    return ('''\
                <ac:structured-macro ac:name="noformat" ac:schema-version="1">
                    <ac:parameter ac:name="nopanel">{nopanel}</ac:parameter>
                    <ac:plain-text-body><![CDATA[{text}]]></ac:plain-text-body>
                </ac:structured-macro>
            ''').format(nopanel=nopanel, text=text)


def symbol_normalizer(text):
    if not text:
        return ""
    result = text
    result = result.replace('&Auml;', u'Ä')
    result = result.replace('&auml;', u'ä')
    result = result.replace('&Euml;', u'Ë')
    result = result.replace('&euml;', u'ë')
    result = result.replace('&Iuml;', u'Ï')
    result = result.replace('&iuml;', u'ï')
    result = result.replace('&Ouml;', u'Ö')
    result = result.replace('&ouml;', u'ö')
    result = result.replace('&Uuml;', u'Ü')
    result = result.replace('&uuml;', u'ü')
    result = result.replace('&Aacute;', u'Á')
    result = result.replace('&aacute;', u'á')
    result = result.replace('&Eacute;', u'É')
    result = result.replace('&eacute;', u'é')
    result = result.replace('&Iacute;', u'Í')
    result = result.replace('&iacute;', u'í')
    result = result.replace('&Oacute;', u'Ó')
    result = result.replace('&oacute;', u'ó')
    result = result.replace('&Uacute;', u'Ú')
    result = result.replace('&uacute;', u'ú')
    result = result.replace('&Agrave;', u'À')
    result = result.replace('&agrave;', u'à')
    result = result.replace('&Egrave;', u'È')
    result = result.replace('&egrave;', u'è')
    result = result.replace('&Igrave;', u'Ì')
    result = result.replace('&igrave;', u'ì')
    result = result.replace('&Ograve;', u'Ò')
    result = result.replace('&ograve;', u'ò')
    result = result.replace('&Ugrave;', u'Ù')
    result = result.replace('&ugrave;', u'ù')
    result = result.replace('&Acirc;', u'Â')
    result = result.replace('&acirc;', u'â')
    result = result.replace('&Ecirc;', u'Ê')
    result = result.replace('&ecirc;', u'ê')
    result = result.replace('&Icirc;', u'Î')
    result = result.replace('&icirc;', u'î')
    result = result.replace('&Ocirc;', u'Ô')
    result = result.replace('&ocirc;', u'ô')
    result = result.replace('&Ucirc;', u'Û')
    result = result.replace('&ucirc;', u'û')
    result = result.replace('&Aring;', u'Å')
    result = result.replace('&aring;', u'å')
    result = result.replace('&deg;', u'°')
    return result
