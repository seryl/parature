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
        self.put_item(url,
                self.get_xml(ticket_data, pretty_print=True))

    def GetCustomer(self, name=None, page=None):
        url = self._create_url('Customer', name)
        if page:
            url += '&_startPage_=%s' % page
        return self.get_item(url)

    def PutCustomer(self, customer_data=None):
        name = customer_data['Customer']['@id']
        url = self._create_url('Customer', name,
                use_json=False)
        self.put_item(url,
                self.get_xml(customer_data, pretty_print=True))

    @staticmethod
    def get_item(url):
        js = JsonXML(url)
        return js.data

    @staticmethod
    def put_item(url, data):
        xmlheader = "<?xml version=\"1.0\" ?>\n"
        url = url.replace('&_output_=json', '')
        parsed_url = urlparse(url)

        conn = httplib.HTTPS(parsed_url.netloc)

        conn.putrequest("PUT", parsed_url.path + '?' + parsed_url.query)
        conn.putheader("Content-Type", "text/xml")
        conn.putheader("Content-Length", str(len(xmlheader+data)))
        conn.endheaders()

        conn.send(xmlheader+data)

        errcode, errmsg, headers = conn.getreply()

        if errcode != 200:
            print '%s, %s, %s' % (errcode, errmsg, headers)

        conn.close()

    def get_xml(self, json_data, pretty_print=False):
        if pretty_print:
            return etree.tostring(
                    self._js.ToXML(data=json_data),
                    pretty_print=True)
        else:
            return etree.tostring(
                    self._js.ToXML(data=json_data))

