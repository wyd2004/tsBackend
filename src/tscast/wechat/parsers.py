from rest_framework.parsers import BaseParser

import xmltodict

class WxPayContentParser(BaseParser):
    media_type = 'text/xml'
    def parse(self, stream, media_type=None, parser_context=None):
        body = stream.read()
        try:
            payload = xmltodict.parse(body)['xml']
        except:
            payload = {}
        return payload
