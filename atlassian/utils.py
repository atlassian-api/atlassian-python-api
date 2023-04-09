# coding=utf-8
import logging
import re

log = logging.getLogger(__name__)


def is_email(element):
    """
    >>> is_email('username@example.com')
    True
    >>> is_email('example.com')
    False
    >>> is_email('firstname.lastname@domain.co.uk')
    True
    """
    email_regex = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
    return re.match(email_regex, str(element))


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
    html = "<ul>"
    for item in data:
        if isinstance(item, dict):
            if item.get("email"):
                item = html_email(item.get("email"), item.get("name", None))
            elif item.get("name"):
                item = item.get("name")

        if is_email(item):
            item = html_email(item, item)
        html += "<li>{}</li>".format(item)
    return html + "</ul>"


def html_table_header_row(data):
    """
    >>> html_table_header_row(['administrators', 'key', 'leader', 'project'])
    '\\n\\t<tr><th>Administrators</th><th>Key</th><th>Leader</th><th>Project</th></tr>'
    >>> html_table_header_row(['key', 'project', 'leader', 'administrators'])
    '\\n\\t<tr><th>Key</th><th>Project</th><th>Leader</th><th>Administrators</th></tr>'
    """
    html = "\n\t<tr>"
    for th in data:
        title = th.replace("_", " ").title()
        html += "<th>{}</th>".format(title)
    return html + "</tr>"


def html_row_with_ordered_headers(data, col_headers, row_header=None):
    """
    >>> headers = ['administrators', 'key', 'leader', 'project']
    >>> data = {'key': 'DEMO', 'project': 'Demonstration',
                'leader': 'leader@example.com',
                'administrators': ['admin1@example.com', 'admin2@example.com']}
    >>> html_row_with_ordered_headers(data, headers)
    '\\n\\t<tr><td><ul>
                        <li><a href="mailto:admin1@example.com">admin1@example.com</a></li>
                        <li><a href="mailto:admin2@example.com">admin2@example.com</a></li>
                    </ul></td><td>DEMO</td><td>leader@example.com</td><td>Demonstration</td></tr>'
    >>> headers = ['key', 'project', 'leader', 'administrators']
    >>> html_row_with_ordered_headers(data, headers)
    '\\n\\t<tr><td>DEMO</td><td>Demonstration</td>
                <td>leader@example.com</td><td>
                <ul>
                    <li><a href="mailto:admin1@example.com">admin1@example.com</a></li>
                    <li><a href="mailto:admin2@example.com">admin2@example.com</a></li>
                </ul></td></tr>'
    """
    html = "\n\t<tr>"
    if row_header:
        html += "<th>{}</th>".format(row_header.replace("_", " ").title())
    for header in col_headers:
        element = data[header]
        if isinstance(element, list):
            element = html_list(element)

        if is_email(element):
            element = html_email(element)
        html += "<td>{}</td>".format(element)
    return html + "</tr>"


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
    html = "<table><tbody>"
    html += html_table_header_row(ordering)
    for row in data:
        html += html_row_with_ordered_headers(row, ordering)
    return html + "\n</tbody></table>"


def html_table_from_nested_dict(data, ordering):
    """
    >>> ordering = ['manager', 'admin', 'employee_count']
    >>>     data = {
        'project_A': {'manager': 'John', 'admin': 'admin1@example.com', 'employee_count': '4'},
        'project_B': {'manager': 'Jane', 'admin': 'admin2@example.com', 'employee_count': '7'}
    }
    >>> html_table_from_nested_dict(data, ordering)
    <table>
        <tbody>
            <tr>
                <th></th>
                <th>Manager</th>
                <th>Admin</th>
                <th>Employee Count</th>
            </tr>
            <tr>
                <th>Project A</th>
                <td>John</td>
                <td><a href="mailto:admin1@example.com">admin1@example.com</a></td>
                <td>4</td>
            </tr>
            <tr>
                <th>Project B</th>
                <td>Jane</td>
                <td><a href="mailto:admin2@example.com">admin2@example.com</a></td>
                <td>7</td>
            </tr>
        </tbody>
    </table>
    """

    html = "<table><tbody>"
    # Add an empty first cell for the row header column
    header_row = [""]
    header_row.extend(ordering)
    html += html_table_header_row(header_row)

    for row_header, row in data.items():
        html += html_row_with_ordered_headers(row, ordering, row_header)

    return html + "\n</tbody></table>"


def block_code_macro_confluence(code, lang=None):
    """
    Wrap into code block macro
    :param code:
    :param lang:
    :return:
    """
    if not lang:
        lang = ""
    return (
        """\
                <ac:structured-macro ac:name="code" ac:schema-version="1">
                    <ac:parameter ac:name="language">{lang}</ac:parameter>
                    <ac:plain-text-body><![CDATA[{code}]]></ac:plain-text-body>
                </ac:structured-macro>
            """
    ).format(lang=lang, code=code)


def html_code__macro_confluence(text):
    """
    Wrap into html macro
    :param text:
    :return:
    """
    return (
        """\
                <ac:structured-macro ac:name="html" ac:schema-version="1">
                    <ac:plain-text-body><![CDATA[{text}]]></ac:plain-text-body>
                </ac:structured-macro>
            """
    ).format(text=text)


def noformat_code_macro_confluence(text, nopanel=None):
    """
    Wrap into code block macro
    :param text:
    :param nopanel: (bool) True or False Removes the panel around the content.
    :return:
    """
    if not nopanel:
        nopanel = False
    return (
        """\
                <ac:structured-macro ac:name="noformat" ac:schema-version="1">
                    <ac:parameter ac:name="nopanel">{nopanel}</ac:parameter>
                    <ac:plain-text-body><![CDATA[{text}]]></ac:plain-text-body>
                </ac:structured-macro>
            """
    ).format(nopanel=nopanel, text=text)


def symbol_normalizer(text):
    if not text:
        return ""
    result = text
    result = result.replace("&Auml;", "Ä")
    result = result.replace("&auml;", "ä")
    result = result.replace("&Euml;", "Ë")
    result = result.replace("&euml;", "ë")
    result = result.replace("&Iuml;", "Ï")
    result = result.replace("&iuml;", "ï")
    result = result.replace("&Ouml;", "Ö")
    result = result.replace("&ouml;", "ö")
    result = result.replace("&Uuml;", "Ü")
    result = result.replace("&uuml;", "ü")
    result = result.replace("&Aacute;", "Á")
    result = result.replace("&aacute;", "á")
    result = result.replace("&Eacute;", "É")
    result = result.replace("&eacute;", "é")
    result = result.replace("&Iacute;", "Í")
    result = result.replace("&iacute;", "í")
    result = result.replace("&Oacute;", "Ó")
    result = result.replace("&oacute;", "ó")
    result = result.replace("&Uacute;", "Ú")
    result = result.replace("&uacute;", "ú")
    result = result.replace("&Agrave;", "À")
    result = result.replace("&agrave;", "à")
    result = result.replace("&Egrave;", "È")
    result = result.replace("&egrave;", "è")
    result = result.replace("&Igrave;", "Ì")
    result = result.replace("&igrave;", "ì")
    result = result.replace("&Ograve;", "Ò")
    result = result.replace("&ograve;", "ò")
    result = result.replace("&Ugrave;", "Ù")
    result = result.replace("&ugrave;", "ù")
    result = result.replace("&Acirc;", "Â")
    result = result.replace("&acirc;", "â")
    result = result.replace("&Ecirc;", "Ê")
    result = result.replace("&ecirc;", "ê")
    result = result.replace("&Icirc;", "Î")
    result = result.replace("&icirc;", "î")
    result = result.replace("&Ocirc;", "Ô")
    result = result.replace("&ocirc;", "ô")
    result = result.replace("&Ucirc;", "Û")
    result = result.replace("&ucirc;", "û")
    result = result.replace("&Aring;", "Å")
    result = result.replace("&aring;", "å")
    result = result.replace("&deg;", "°")
    return result


def parse_cookie_file(cookie_file):
    """
    Parse a cookies.txt file (Netscape HTTP Cookie File)
    return a dictionary of key value pairs
    compatible with requests.
    :param cookie_file: a cookie file
    :return dict of cookies pair
    """
    cookies = {}
    with open(cookie_file, "r") as fp:
        for line in fp:
            if not re.match(r"^(#|$)", line):
                line_fields = line.strip().split("\t")
                try:
                    cookies[line_fields[5]] = line_fields[6]
                except IndexError as e:
                    log.error(e)
    return cookies
