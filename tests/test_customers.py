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
        cust = Customer (
            first_name="Marry", 
            last_name="Wang", 
            user_id="marrywang", 
            password="password", 
            address_id="100",
        )
        self.assertTrue(cust != None)
        self.assertEqual(cust.customer_id, None)
        self.assertEqual(cust.first_name, "Marry")
        self.assertEqual(cust.last_name, "Wang")
        self.assertEqual(cust.user_id, "marrywang")
        self.assertEqual(cust.password, "password")
        self.assertEqual(cust.address_id, "100")

    def test_create_a_address(self):
        """ Create an address and assert that it exists """
        addr = Address (
            street="100 W 100th St.",
            apartment="100",
            city="New York",
            state="New York",
            zip_code="10035",
        )
        self.assertTrue(addr != None)
        self.assertEqual(addr.id, None)
        self.assertEqual(addr.street, "100 W 100th St.")
        self.assertEqual(addr.apartment, "100")
        self.assertEqual(addr.city, "New York")
        self.assertEqual(addr.zip_code, "10035")

    def test_add_a_customer(self):
        """ Create a address and add it to the database, then 
        create a customer with the address.id and add it to the database 
        """
        custs = Customer.all()
        self.assertEqual(custs, [])
        cust = Customer (
            first_name="Marry", 
            last_name="Wang", 
            user_id="marrywang", 
            password="password", 
            active = True
        )
        self.assertTrue(cust != None)
        self.assertEqual(cust.customer_id, None)
        self.assertEqual(cust.address_id, None)
        
        cust.save()

        addr = Address (
            street="100 W 100th St.",
            apartment="100",
            city="New York",
            state="New York",
            zip_code="10035",
        )
        addr.save()
        cust.address_id = addr.id
        addr.customer_id = cust.customer_id
         # Asert that it was assigned an id and shows up in the database
        self.assertEqual(addr.id, 1)
        custs = Customer.all()
        self.assertEqual(len(custs), 1)

        self.assertEqual(cust.customer_id, 1)
        custs = Customer.all()
        self.assertEqual(len(custs), 1)
    
    def test_serialize_a_customer(self):
        """ Test serialization of a customer """
        cust = Customer (
            first_name="Marry", 
            last_name="Wang", 
            user_id="marrywang", 
            password="password", 
        )
        data = cust.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('first name', data)
        self.assertEqual(data['first name'], "Marry")
        self.assertIn('last name', data)
        self.assertEqual(data['last name'], "Wang")
        self.assertIn('user id', data)
        self.assertEqual(data['user id'], "marrywang")

    def test_deserialize_a_customer(self):
        """ Test deserialization of a customer """
        data = {
            "first_name": "Marry", 
            "last_name": "Wang",
            "user_id": "marrywang", 
            "password": "password"
        }
        cust = Customer()
        cust.deserialize(data)
        self.assertNotEqual(cust, None)
        self.assertEqual(cust.customer_id, None)
        self.assertEqual(cust.first_name, "Marry")
        self.assertEqual(cust.last_name, "Wang")
        self.assertEqual(cust.user_id, "marrywang")
        self.assertEqual(cust.password, "password")
    
    def test_serialize_an_address(self):
        """ Test serialization of a customer """
        addr = Address (
            street = "100 W 100 St.",
            apartment = "100",
            city = "New York",
            state = "New York",
            zip_code = "100"
        )
        data = addr.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('street', data)
        self.assertEqual(data['street'], "100 W 100 St.")
        self.assertIn('apartment', data)
        self.assertEqual(data['apartment'], "100")
        self.assertIn('city', data)
        self.assertEqual(data['city'], "New York")
        self.assertIn('state', data)
        self.assertEqual(data['state'], "New York")
        self.assertIn('zip code', data)
        self.assertEqual(data['zip code'], "100")

    def test_deserialize_an_address(self):
        """ Test deserialization of a customer """
        data = {
            "street": "100 W 100 St.",
            "apartment": "100",
            "city": "New York",
            "state": "New York",
            "zip_code": "100"
        }
        addr = Address()
        addr.deserialize(data)
        self.assertNotEqual(addr, None)
        self.assertEqual(addr.customer_id, None)
        self.assertEqual(addr.street, "100 W 100 St.")
        self.assertEqual(addr.apartment, "100")
        self.assertEqual(addr.city, "New York")
        self.assertEqual(addr.state, "New York")
        self.assertEqual(addr.zip_code, "100")

    # def test_deserialize_bad_data(self):
    #     """ Test deserialization of bad data """
    #     data = "this is not a dictionary"
    #     pet = Pet()
    #     self.assertRaises(DataValidationError, pet.deserialize, data)
