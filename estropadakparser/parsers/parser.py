import lxml.html
import urllib.request


class Parser(object):

    def __init__(self):
        pass

    def _prepare_request(self, url: str) -> urllib.request.Request:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT x.y; rv:10.0) Gecko/20100101 Firefox/10.0"
        }
        r = urllib.request.Request(url, headers=headers)
        return r

    def get_content(self, *args):
        '''Get content from URL or HTML string'''
        urla = args[0]
        if len(args) == 2 and args[1] is not None:
            document = lxml.html.fromstring(args[1])
        else:
            r = self._prepare_request(urla)
            html_file = urllib.request.urlopen(r)
            content = html_file.read()
            document = lxml.html.fromstring(content)
        return document