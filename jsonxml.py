# Author: Josh Toft
# Email: josh@rockyou.com
#
# Based on the Article:
# http://www.xml.com/pub/a/2006/05/31/converting-between-xml-and-json.html

import json
from urllib import urlopen
from lxml import etree

class JsonXML(object):
    def __init__(self, url=None, use_json=True):
        if url:
            if use_json:
                self.data = str(unicode(
                    urlopen(url).read(),
                    errors='ignore'))
                self.data = json.loads(self.data)
                if self.data.has_key('?xml'):
                    del(self.data['?xml'])

    def ToXML(self, data=None):
        et = None
        if not data:
            data = self.data
        for k,v in data.iteritems():
            et = etree.Element(k)
            et = self.__build_xml_tree__(v, et)
        return et

    @staticmethod
    def __build_xml_tree__(json_data, parent):
        if isinstance(json_data, unicode):
            parent.text = json_data
            return parent
        for k,v in json_data.iteritems():
            if k.startswith('@'):
                parent.set(k[1:], v)
            elif k.startswith('#'):
                parent.text = v
            else:
                if isinstance(v, list):
                    for item in v:
                        child = etree.SubElement(parent, k)
                        if not item:
                            continue
                        child = JsonXML.__build_xml_tree__(
                                item, child)
                else:
                    child = etree.SubElement(parent, k)
                    if v:
                        child = JsonXML.__build_xml_tree__(
                                v, child)
        return parent

