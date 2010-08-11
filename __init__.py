# Author: Josh Toft
# Email: josh@rockyou.com
#
import httplib

from decorator import decorator
from jsonxml import JsonXML
from lxml import etree
from time import sleep
from math import ceil

from urllib import urlopen, urlencode
from urlparse import urlparse

@decorator
def throttle_requests(func, *args, **kwargs):
    # limit to 110 req/s
    sleep(0.0018333333333333333)
    return func(*args, **kwargs)

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

    def GetTicket(self, name=None, page=None, page_size=None):
        url = self._create_url('Ticket', name)
        if name:
            return self.get_item(url)
        if page_size:
            url += '&_pageSize_=%s' % page_size
        if page:
            url += '&_startPage_=%s' % page
        return self.get_item(url)

    def GetTicketList(self, page_size=None):
        initial_list = self.GetTicket(page_size=page_size)
        page_size = int(initial_list['Entities']['@page-size'])
        total_tickets = int(initial_list['Entities']['@total'])
        total_page_count = int(ceil((total_tickets + 0.0)/page_size))
        for cur_page in xrange(1, total_page_count+1):
            if cur_page==1:
                ticket_list = initial_list
            else:
                ticket_list = self.GetTicket(
                        page=cur_page, page_size=page_size)
            for k,v in ticket_list['Entities'].items():
                if k == 'Ticket':
                    for ticket in v:
                        yield ticket

    def PutTicket(self, ticket_data=None):
        name = ticket_data['Ticket']['@id']
        url = self._create_url('Ticket', name,
                use_json=False)
        self.put_item(url, ticket_data)

    def GetCustomer(self, name=None, page=None, page_size=None):
        url = self._create_url('Customer', name)
        if name:
            return self.get_item(url)
        if page_size:
            url += '&_pageSize_=%s' % page_size
        if page:
            url += '&_startPage_=%s' % page
        return self.get_item(url)

    def GetCustomerList(self, page_size=None):
        initial_list = self.GetCustomer(page_size=page_size)
        page_size = int(initial_list['Entities']['@page-size'])
        total_customers = int(initial_list['Entities']['@total'])
        total_page_count = int(ceil((total_customers + 0.0)/page_size))
        for cur_page in xrange(1, total_page_count+1):
            if cur_page == 1:
                customer_list = initial_list
            else:
                customer_list = self.GetCustomer(
                        page=cur_page, page_size=page_size)
            for k,v in customer_list['Entities'].items():
                if k == 'Customer':
                    for customer in v:
                        yield customer

    def PutCustomer(self, customer_data=None):
        name = customer_data['Customer']['@id']
        url = self._create_url('Customer', name,
                use_json=False)
        self.put_item(url, customer_data)

    @staticmethod
    @throttle_requests
    def get_item(url):
        js = JsonXML(url)
        return js.data

    @throttle_requests
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

