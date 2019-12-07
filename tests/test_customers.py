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
from service.service import app, init_db


# DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://postgres:postgres@localhost:5432/postgres')
DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://jpklhqur:Zm9vW9NAoSSrcVtIbZm8NisKnUxJG-a4@rajje.db.elephantsql.com:5432/jpklhqur')

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
        if DATABASE_URI:
            app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
        db.drop_all()   # clean before all tests
        init_db()

    @classmethod
    def tearDownClass(cls):
        # db.drop_all()   # clean up after the last test
        db.session.remove() # disconnect from database

    def setUp(self):
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
            customer_id=1
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
        addr.customer_id = cust.customer_id
        addr.save()
        cust.address_id = addr.id
         # Asert that it was assigned an id and shows up in the database
        self.assertEqual(addr.id, 1)
        custs = Customer.all()
        self.assertEqual(len(custs), 1)

        self.assertEqual(cust.customer_id, 1)
        custs = Customer.all()
        self.assertEqual(len(custs), 1)

    def test_update_a_customer(self):
        """ Update a customer """
        customer = Customer(first_name="Marry", last_name="Wang", user_id="marrywang", password="password", active = True, address_id=100)
        customer.save()
        self.assertEqual(customer.customer_id, 1)
        # Change it an save it
        customer.password = "DevOps is awesome"
        customer.save()
        self.assertEqual(customer.customer_id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customer = Customer.all()
        self.assertEqual(len(customer), 1)
        self.assertEqual(customer[0].password, "DevOps is awesome")

    def test_delete_a_customer(self):
        """ Delete a customer """
        customer = Customer(first_name="Marry", last_name="Wang", user_id="marrywang", password="password", active = True)
        customer.save()
        address = Address(street = "100 W 100 St.", apartment = "100", city = "New York", state = "New York", zip_code = "100")
        address.customer_id = customer.customer_id
        address.save()
        customer.address_id = address.id
        customer.save()

        self.assertEqual(len(Customer.all()), 1)
        self.assertEqual(len(Address.all()), 1)

        # delete the customer and make sure it isn't in the database
        customer.delete()
        self.assertEqual(len(Customer.all()), 0)
        self.assertEqual(len(Address.all()), 0)

    def test_list_all_customers(self):
        """ Create two customers and add them to the database, then
            obtain list of all customers and ensure it is = 2
        """
        cust1 = Customer (
            first_name="Jane",
            last_name="Doe",
            user_id="janedoe",
            password="Asdf@1234",
            active = True
        )
        cust1.save()

        cust2 = Customer (
            first_name="John",
            last_name="Doe",
            user_id="johndoe",
            password="Asdf@1234",
            active = True,
        )
        cust2.save()
        all_customers = Customer.all()
        self.assertEquals(len(all_customers), 2)

    def test_serialize_a_customer(self):
        """ Test serialization of a customer """
        cust = Customer (
            first_name="Marry",
            last_name="Wang",
            user_id="marrywang",
            password="password",
            active=True,
        )
        cust.save()
        addr = Address(
            street="48 John St",
            apartment="1B",
            city="New York",
            state="New York",
            zip_code="22890",
            customer_id=cust.customer_id,
        )
        addr.save()
        cust.address_id=addr.id
        cust.save()
        data = cust.serialize()
        self.assertNotEqual(data, None)
        self.assertIn('first_name', data)
        self.assertEqual(data['first_name'], "Marry")
        self.assertIn('last_name', data)
        self.assertEqual(data['last_name'], "Wang")
        self.assertIn('user_id', data)
        self.assertEqual(data['user_id'], "marrywang")

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
        self.assertEqual(data['state'], "New York")
        self.assertIn('state', data)
        self.assertIn('zip_code', data)
        self.assertEqual(data['zip_code'], "100")

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

    def test_deserialize_address_key_error(self):
        """ Test address deserialization from incomplete data """
        data = {
            "street": "100 W 100 St.",
            "apartment": "100",
            "state": "New York",
            "zip_code": "100"
        }
        addr = Address()
        with self.assertRaises(DataValidationError) as error:
            addr.deserialize(data)
        self.assertEqual(str(error.exception), 'Invalid address: '\
                         'missing city')

    def test_find_customer(self):
        """ Find active/inactive customers with filter """
        active_customer = Customer (
            first_name="Peter",
            last_name="Parker",
            user_id="pparker",
            password="password",
            active = True
        )
        active_customer.save()

        inactive_customer = Customer (
            first_name="Peter.B.",
            last_name="Parker",
            user_id="pbparker",
            password="password",
            active = False
        )
        inactive_customer.save()

        """ Find active customers with filter """
        result_active_filter = Customer.find(active_customer.user_id)
        self.assertEqual(result_active_filter[0].user_id, active_customer.user_id)

        """ Find active customers with filter """
        result_active_no_filter = Customer.find(active_customer.user_id)
        self.assertEqual(result_active_no_filter[0].user_id, active_customer.user_id)

        """ Find inactive customers with filter """
        result_inactive_filter = Customer.find(inactive_customer.user_id)
        self.assertEqual(result_inactive_filter[0].user_id, inactive_customer.user_id)

        """ Find inactive customers with filter """
        result_inactive_no_filter = Customer.find(inactive_customer.user_id)
        self.assertEqual(result_inactive_no_filter[0].user_id, inactive_customer.user_id)

        def test_queries(self):
            """ Find active/inactive customers with filter """
            cust = Customer(
                first_name="Peter",
                last_name="Parker",
                user_id="pparker",
                password="password",
                active = True
            )
            cust.save()
            addr = Address(
                apartment="1R",
                city="Chicago",
                state="Illinois",
                street="6721 5th Ave",
                zip_code="10030",
                customer_id=cust.customer_id
            )
            addr.save()
            cust.address_id = addr.id
            cust.save()
            """ Find by first name """
            cust_fname = Customer.find_by_first_name(cust.first_name)
            self.assertEqual(cust_fname[0].customer_id, cust.customer_id)

            """ Find by last name """
            cust_lname = Customer.find_by_last_name(cust.last_name)
            self.assertEqual(cust_lname[0].customer_id, cust.customer_id)

            """ Find by status """
            cust_active = Customer.find_by_status(False)
            self.assertEqual(len(cust_active), 0)

            """ Find by city """
            cust_city = Address.find_by_city(cust.city)
            self.assertEqual(cust_city[0].customer_id, cust.customer_id)

            """ Find by state """
            cust_state = Address.find_by_state(cust.state)
            self.assertEqual(cust_state[0].customer_id, cust.customer_id)

            """ Find by zip code """
            cust_zip = Address.find_zip(cust.zip_code)
            self.assertEqual(cust_zip[0].customer_id, cust.customer_id)

    def test_remove_all_customers(self):
        """ Remove all customers """
        customer = Customer(first_name="Marry", last_name="Wang", user_id="marrywang", password="password", active = True, address_id=100)
        customer.save()
        customer = Customer(first_name="Marry", last_name="Jane", user_id="marryjane", password="password", active = True, address_id=200)
        customer.save()
        all_customers = Customer.all()
        self.assertEquals(len(all_customers), 2)
        customer.remove_all()
        all_customers = Customer.all()
        self.assertEquals(len(all_customers), 0)

    def test_remove_all_addresses(self):
        """ Remove all addresses """
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
        addr.customer_id = cust.customer_id
        addr.save()
        all_addresses = Address.all()
        self.assertEquals(len(all_addresses), 1)

        addr.remove_all()
        all_addresses = Address.all()
        self.assertEquals(len(all_addresses), 0)

