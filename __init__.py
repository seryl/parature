# Author: Josh Toft
# Email: josh@rockyou.com
#
import httplib

from jsonxml import JsonXML
from lxml import etree

from urllib import urlopen, urlencode
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
        name = ticket_data['Ticket']['@id']
        url = self._create_url('Ticket', name,
                use_json=False)
        self.put_item(url, ticket_data)

    def GetCustomer(self, name=None, page=None):
        url = self._create_url('Customer', name)
        if page:
            url += '&_startPage_=%s' % page
        return self.get_item(url)

    def PutCustomer(self, customer_data=None):
        name = customer_data['Customer']['@id']
        url = self._create_url('Customer', name,
                use_json=False)
        self.put_item(url, customer_data)

    @staticmethod
    def get_item(url):
        js = JsonXML(url)
        return js.data

    def put_item(self, url, data):
        headers = {'Content-Type': 'text/xml'}
        parsed_url = urlparse(url)
        data = self.get_xml(data, pretty_print=True)

        conn = httplib.HTTPSConnection(parsed_url.netloc)
        conn.request("PUT",
                parsed_url.path + '?' + parsed_url.query,
                data, headers)

        resp = conn.getresponse()
        if resp.status not in [200, 201]:
            print resp.status, resp.reason
            print resp.read()

        conn.close()

    def get_xml(self, json_data, pretty_print=False):
        if pretty_print:
            return etree.tostring(
                    self._js.ToXML(data=json_data),
                    pretty_print=True)
        else:
            return etree.tostring(
                    self._js.ToXML(data=json_data))

