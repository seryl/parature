import httplib

from jsonxml import JsonXML
from lxml import etree

from urllib import urlopen
from urlparse import urlparse

class Parature(object):
    def __init__(self, hostname, client_id, dept_id, token):
        self._hostname = hostname
        self._client_id = client_id
        self._dept_id = dept_id
        self._token = token
        self._base_url = 'https://%s/api/v1/%s/%s/' % (
                hostname, client_id, dept_id)
        self._js = JsonXML()

    def _create_url(self, selector, name, use_json=True):
        url = self._base_url + selector
        if name:
            url += '/%s' % name
        url += '?_token_=%s' % self._token
        if use_json:
            url += '&_output_=json'
        return url

    def GetTicket(self, name=None, page=None):
        url = self._create_url('Ticket', name)
        if page:
            url += '&_startPage_=%s' % page
        return self.get_item(url)

    def PutTicket(self, ticket_data=None):
        name = None
        # name = parse ticket id here
        url = self._create_url('Ticket', name,
                use_json=False)

    def GetCustomer(self, name=None, page=None):
        url = self._create_url('Customer', name)
        if page:
            url += '&_startPage_=%s' % page
        return self.get_item(url)

    def PutCustomer(self, customer_data=None):
        name = None
        # name = parse customer id here
        url = self._create_url('Customer', name,
                use_json=False)
        put_item(url, customer_data)

    @staticmethod
    def get_item(url):
        js = JsonXML(url)
        return js.data

    @staticmethod
    def put_item(url, data):
        parsed_url = urlparse(url)
        headers = { 'Content-Type': "text/xml" }
        conn = httplib.HTTPS(parsed_url.netloc)
        conn.request("PUT",
                     parse_url.netloc + \
                         parsed_url.path + \
                         '?' + parse_url.query,
                     data, headers)
        response = conn.getresponse()
        print response.status, response.reason, response.read()
        conn.close()

    def get_xml(self, json_data, pretty_print=False):
        if pretty_print:
            return etree.tostring(
                    self._js.ToXML(data=json_data),
                    pretty_print=True)
        else:
            return etree.tostring(
                    self._js.ToXML(data=json_data))

