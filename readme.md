Python Parature API
===================

API for [Parature](http://www.parature.com/ "Parature")

Example usage:

    from parature import Parature
    
    class YourParatureClass(Parature):
        def __init__(self):
            parature_connection = {
                'hostname': 'your_server.parature.com',
                'client_id': your_client_id,
                'dept_id': your_dept_id,
                'token':, 'yourtokenhere'
            }
            super(YourParatureClass, self).__init__(**parature_connection)
    
        def test(self):
            # GET Examples
            
            # Get all of the customers (Generator)
            customerlist = self.GetCustomerList()
            for customer in customerlist:
                print customer
    
            # Get a single customer (By id)
            customer = self.GetCustomer(1)
            print customer
   
            # Get all of the tickets (Generator) 
            ticketlist = self.GetTicketList()
            for ticket in ticketlist:
                print ticket
    
            # Get a single ticket (By id)
            ticket = self.GetTicket(1)
            print ticket
    
            # Put Example (Update a customer)
            customer['Customer']['First_Name'] = 'Jane'
            self.PutCustomer(customer)
             
This of course can be expanded, and just wanted to post something so people would have a general idea of how the api functions.

