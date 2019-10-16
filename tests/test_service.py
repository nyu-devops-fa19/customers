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
from flask_api import status    # HTTP Status Codes
from unittest.mock import MagicMock, patch
from service.models import Customer, Address, DataValidationError, db
from tests.customer_factory import CustomerFactory, AddressFactory
from service.service import app, init_db, initialize_logging

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

    count = 10

    def test_update_customer(self):
        """ Update an existing Customer """
        # create a customer to update
        test_customer = CustomerFactory()
        test_address = AddressFactory()
        test_customer.save()
        test_address.customer_id = test_customer.customer_id
        test_address.save()
        test_customer.address_id = test_address.id
        test_customer.save()
        # update the customer
        test_customer.first_name = 'Cow'
        resp = self.app.put('/customers/{}'.format(test_customer.user_id),
                            json=test_customer.internal_serialize(),
                            content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_customer = resp.get_json()
        self.assertEqual(updated_customer['first_name'], 'Cow')

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

    def test_deactivate_customer(self):
        """ Deactivate a customer """
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


