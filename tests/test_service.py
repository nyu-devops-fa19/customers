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
Customer API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
  codecov --token=$CODECOV_TOKEN
"""

import unittest
import os
import logging
import uuid
from flask_api import status    # HTTP Status Codes
from unittest.mock import MagicMock, patch
from service.models import Customer, Address, DataValidationError, db
from tests.customer_factory import CustomerFactory, AddressFactory
from service.service import app, init_db, initialize_logging, internal_server_error

#DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv('DATABASE_URI', 'postgres://postgres:passw0rd@localhost:5432/postgres')

######################################################################
#  T E S T   C A S E S
######################################################################
class TestCustomerServer(unittest.TestCase):
    """ Customer Server Tests """

    @classmethod
    def setUpClass(cls):
        """ Run once before all tests """
        app.debug = False
        initialize_logging(logging.INFO)
        # Set up the test database
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        """ Runs before each test """
        init_db()
        db.drop_all()    # clean up the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def _create_customers(self, count):
        """ Factory method to create customers in bulk """
        customers = []
        for _ in range(count):
            test_customer = CustomerFactory()
            test_address = AddressFactory()
            addr_json = test_address.serialize()
            cust_json = test_customer.internal_serialize()
            cust_json["address"] = addr_json
            resp = self.app.post('/customers',
                                 json=cust_json,
                                 content_type='application/json')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED, 'Could not create test customer')
            new_cust = resp.get_json()
            test_customer.id = new_cust["customer_id"]
            addr = new_cust["address"]
            test_customer.address_id = addr["id"]
            customers.append(test_customer)
        return customers

    def test_create_customer_400_missing_uid(self):
        body = {
            "first_name": "Luke",
            "last_name": "Yang",
            "password": "password",
            "address": {
                "street": "100 W 100 St.",
                "apartment": "100",
                "city": "New York",
                "state": "New York",
                "zip_code": "100"
            }
        }
        """ Test wrong request when creating a customer - missing user_id """
        resp = self.app.post('/customers', json=body, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cust_not_found_404(self):
        """ Test retrieving a Customer that does not exist"""
        customers = self._create_customers(1)
        resp = self.app.get('/customers/{}'.format("xyz"),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_customer(self):
        """create a new customer"""
        body = {
            "first_name": "Luke",
            "last_name": "Yang",
            "user_id": "lukeyang",
            "password": "password",
            "address": {
                "street": "100 W 100 St.",
                "apartment": "100",
                "city": "New York",
                "state": "New York",
                "zip_code": "100"
            }
        }
        resp = self.app.post('/customers',
                             json=body,
                             content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get('Location', None)
        self.assertTrue(location != None)
        # Check the data is correct
        new_customer = resp.get_json()
        self.assertEqual(new_customer['first_name'], "Luke", "first_name do not match")
        self.assertEqual(new_customer['last_name'], "Yang", "last_name do not match")
        self.assertEqual(new_customer['user_id'], "lukeyang", "user_id do not match")
        self.assertEqual(new_customer['active'], True, "active status not match")

        resp = self.app.get(location,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_customer = resp.get_json()[0]
        self.assertEqual(new_customer['first_name'], "Luke", "first_name do not match")
        self.assertEqual(new_customer['last_name'], "Yang", "last_name do not match")
        self.assertEqual(new_customer['user_id'], "lukeyang", "user_id do not match")
        self.assertEqual(new_customer['active'], True, "active status not match")

    def test_update_customer(self):
        """ Update an existing Customer """
        # create a customer to update
        customers = self._create_customers(1)
        test_customer = customers[0]
        test_customer.first_name = 'Cow'
        cust_json = test_customer.internal_serialize()
        cust_json["address"] = Address.find(test_customer.address_id)
        resp = self.app.put('/customers/{}'.format(test_customer.user_id),
                            json=cust_json,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_customer = resp.get_json()
        self.assertEqual(updated_customer['first_name'], 'Cow')

    def _create_customer(self):
        """ create a customer for testing delete"""
        test_customer = {
            "first_name": "Luke",
            "last_name": "Yang",
            "user_id": "lukeyang",
            "password": "password",
            "address": {
                "street": "100 W 100 St.",
                "apartment": "100",
                "city": "New York",
                "state": "New York",
                "zip_code": "100"
            }
        }
        resp = self.app.post('/customers',
                            json=test_customer,
                            content_type='application/json')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, 'Could not create test customer')
        new_customer = resp.get_json()

        return new_customer

    def test_delete_customer(self):
        # create a customer to update
        test_customer = self._create_customer()
        """ Delete a Customer """
        resp = self.app.delete('/customers/{}'.format(test_customer['user_id']),
                               content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get('/customers/{}'.format(test_customer['user_id']),
                            content_type='application/json')

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_deactivate_customer(self):
        """ Deactivate an existing customer """
        # create a customer to deactivate
        body = {
            "first_name": "Peter",
            "last_name": "Parker",
            "user_id": "pparker",
            "password": "withGreatPower",
            "address": {
                "street": "20 Ingram Street",
                "apartment": "FL 2",
                "city": "Flushing",
                "state": "New York",
                "zip_code": "11375"
            }
        }
        resp_create = self.app.post('/customers',
                             json=body,
                             content_type='application/json')
        self.assertEqual(resp_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp_create.get_json()['active'], True)

        # deactivate the customer
        resp_deactivate = self.app.put('/customers/pparker/deactivate',
                             json=body,
                            content_type='application/json')
        self.assertEqual(resp_deactivate.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_deactivate.get_json()['active'], False)

    def test_get_customer_list(self):
        """ Get a list of Customers """
        self._create_customers(5)
        resp = self.app.get('/customers')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 5)

    def test_get_by_user_id(self):
        """ Get customer by user_id """
        customers = self._create_customers(10)
        test_user_id = customers[0].user_id
        user_id_customers = [cust for cust in customers if cust.user_id == test_user_id]
        resp = self.app.get('/customers/{}'.format(test_user_id),
                            content_type='application/json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(user_id_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['user_id'], test_user_id)

    def test_query_by_fname(self):
        """ Query Customers by First Name """
        customers = self._create_customers(10)
        test_fname = customers[0].first_name
        fname_customers = [cust for cust in customers if cust.first_name == test_fname]
        resp = self.app.get('/customers',
                            query_string='fname={}'.format(test_fname))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(fname_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['first_name'], test_fname)

    def test_query_by_lname(self):
        """ Query Customers by Last Name """
        customers = self._create_customers(10)
        test_lname = customers[0].last_name
        lname_customers = [cust for cust in customers if cust.last_name == test_lname]
        resp = self.app.get('/customers',
                            query_string='lname={}'.format(test_lname))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(lname_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['last_name'], test_lname)

    def test_query_by_city(self):
        """ Query Customers by City """
        customers = self._create_customers(10)
        test_city = Address.find(customers[0].address_id)['city']
        city_customers = [cust for cust in customers if Address.find(cust.address_id)['city'] == test_city]
        resp = self.app.get('/customers',
                            query_string='city={}'.format(test_city))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(city_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['address']['city'], test_city)

    def test_query_by_state(self):
        """ Query Customers by State """
        customers = self._create_customers(10)
        test_state = Address.find(customers[0].address_id)['state']
        state_customers = [cust for cust in customers if Address.find(cust.address_id)['state'] == test_state]
        resp = self.app.get('/customers',
                            query_string='state={}'.format(test_state))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(state_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['address']['state'], test_state)

    def test_query_by_zip(self):
        """ Query Customers by Zip Code """
        customers = self._create_customers(10)
        test_zip = Address.find(customers[0].address_id)['zip_code']
        zip_customers = [cust for cust in customers if Address.find(cust.address_id)['zip_code'] == test_zip]
        resp = self.app.get('/customers',
                            query_string='zip={}'.format(test_zip))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), len(zip_customers))
        # check the data just to be sure
        for customer in data:
            self.assertEqual(customer['address']['zip_code'], test_zip)

    def test_activate_customer(self):
        """ Activate an existing customer """
        # create a customer to activate
        body = {
            "first_name": "Gwen",
            "last_name": "Stacy",
            "user_id": "gstacy",
            "password": "heyGuys",
            "address": {
                "street": "20 Ingram Street",
                "apartment": "FL 2",
                "city": "Flushing",
                "state": "New York",
                "zip_code": "11375"
            }
        }
        resp_create = self.app.post('/customers',
                             json=body,
                             content_type='application/json')
        self.assertEqual(resp_create.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp_create.get_json()['active'], True)

        # deactivate the customer
        resp_deactivate = self.app.put('/customers/gstacy/deactivate',
                             json=body,
                            content_type='application/json')
        self.assertEqual(resp_deactivate.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_deactivate.get_json()['active'], False)

        # activate the customer
        resp_activate = self.app.put('/customers/gstacy/activate',
                             json=body,
                            content_type='application/json')
        self.assertEqual(resp_activate.status_code, status.HTTP_200_OK)
        self.assertEqual(resp_activate.get_json()['active'], True)

    def test_deactivate_customer_not_found(self):
        """ Deactivate a non-existing customer """
        body = {
            "first_name": "Gwen",
            "last_name": "Stacy",
            "user_id": "gstacy",
            "password": "heyGuys",
            "address": {
                "street": "20 Ingram Street",
                "apartment": "FL 2",
                "city": "Flushing",
                "state": "New York",
                "zip_code": "11375"
            }
        }
        resp_deactivate = self.app.put('/customers/bwayne/deactivate',
                             json=body,
                            content_type='application/json')
        self.assertEqual(resp_deactivate.status_code, status.HTTP_404_NOT_FOUND)

    def test_activate_customer_not_found(self):
        """ Activate a non-existing customer """
        body = {
            "first_name": "Gwen",
            "last_name": "Stacy",
            "user_id": "gstacy",
            "password": "heyGuys",
            "address": {
                "street": "20 Ingram Street",
                "apartment": "FL 2",
                "city": "Flushing",
                "state": "New York",
                "zip_code": "11375"
            }
        }
        resp_activate = self.app.put('/customers/bwayne/activate',
                             json=body,
                            content_type='application/json')
        self.assertEqual(resp_activate.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_customer_not_found(self):
        """ Update a non-existing Customer """
        body = {
            "first_name": "Gwen",
            "last_name": "Stacy",
            "user_id": "gstacy",
            "password": "heyGuys",
            "address": {
                "street": "20 Ingram Street",
                "apartment": "FL 2",
                "city": "Flushing",
                "state": "New York",
                "zip_code": "11375"
            }
        }
        resp = self.app.put('/customers/bwayne',
                            json=body,
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_invalid_content_type(self):
        """ Invalid content type """
        body = {
            "first_name": "Gwen",
            "last_name": "Stacy",
            "user_id": "gstacy",
            "password": "heyGuys",
            "address": {
                "street": "20 Ingram Street",
                "apartment": "FL 2",
                "city": "Flushing",
                "state": "New York",
                "zip_code": "11375"
            }
        }
        resp = self.app.put('/customers/{}',
                            json=body,
                            content_type='text/plain')
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_root_index(self):
        """ Test root index result """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data['name'], 'Customers REST API Service')
        self.assertEqual(data['version'], '1.0')

    @patch('service.models.Customer.delete')
    def test_internal_server_error_500(self, request_mock):
        """ Internal server error """
        request_mock.delete.side_effect = internal_server_error("error")
        resp = self.app.delete('/customers/JoJo')
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_invalid_method_request_405(self):
        """ Method not supported error """
        resp = self.app.delete('/customers', content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_customer_415(self):
        """ Test creating a customer with unsupported content type """
        resp = self.app.post('/customers', data={
            'first_name': 'cust_first_name',
            'last_name': 'cust_last_name',
            'customer_id': 100,
        }, headers={'content-type': 'text/plain'})
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

    def test_rename_customer_invalid_content_type(self):
        """ Test renaming a wishlist with invalid content type """
        customer = Customer(first_name="Marry", last_name="Wang", user_id="newname", password="password", active = True, address_id=100)
        customer.save()
        resp = self.app.put('/customers/%s' % customer.user_id, json={
            'user_id': 'newname'
        }, headers={'content-type': 'text/plain'})
        self.assertEqual(resp.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
