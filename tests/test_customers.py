# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Customer Model

Test cases can be run with:
  nosetests
  coverage report -m
"""

import unittest
import os
from werkzeug.exceptions import NotFound
from service.models import Customer, Address, DataValidationError, db
from service import app

DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://postgres:passw0rd@localhost:5432/postgres')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestCustomers(unittest.TestCase):
    """ Test Cases for Customers """

    @classmethod
    def setUpClass(cls):
        """ These run once per Test suite """
        app.debug = False
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        Customer.init_db(app)
        Address.init_db(app)
        db.drop_all()    # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_a_customer(self):
        """ Create a customer and assert that it exists """
        # addr = Address (
        #   	street= "100 W 100 St.",
		    #     apartment= "100",
		    #     city= "New York",
		    #     state= "New York",
		    #     zip_code= "100",
        # )
        cust = Customer(first_name="Marry", last_name="Wang", user_id="marrywang", password="password", address_id="100")
        self.assertTrue(cust != None)
        self.assertEqual(cust.customer_id, None)
        self.assertEqual(cust.first_name, "Marry")
        self.assertEqual(cust.last_name, "Wang")
        self.assertEqual(cust.user_id, "marrywang")
        self.assertEqual(cust.password, "password")
        self.assertEqual(cust.address_id, "100")

    
    def test_delete_a_customer(self):
        """ Delete a customer """
        customer = Customer(first_name="Marry", last_name="Wang", user_id="marrywang", password="password", active = True, address_id=100)
        address = Address(street = "100 W 100 St.", apartment = "100", city = "New York", state = "New York", zip_code = "100")
        customer.save()
        address.save()
        self.assertEqual(len(Customer.all()), 1)
        self.assertEqual(len(Address.all()), 1)
        
        # delete the customer and make sure it isn't in the database
        customer.delete()
        address.delete()
        self.assertEqual(len(Customer.all()), 0)
        self.assertEqual(len(Address.all()), 0)







