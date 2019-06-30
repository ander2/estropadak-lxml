import lxml.html
import urllib.request


class Parser(object):

    def __init__(self):
        pass

    def get_content(self, *args):
        '''Get content from URL or HTML string'''
        urla = args[0]
        if len(args) == 2 and args[1] is not None:
            document = lxml.html.fromstring(args[1])
        else:
            html_file = urllib.request.urlopen(urla)
            content = html_file.read()
            document = lxml.html.fromstring(content)
        return document