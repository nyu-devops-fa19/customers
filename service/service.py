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
Paths:
------
GET /customers - returns a list all of the Customers
GET /customers/{user_id} - returns the Customer with a given user_id
POST /customers - creates a new Customer record in the database
PUT /customers/{user_id} - updates a Customer record in the database
DELETE /customers/{user_id} - deletes a Customer record in the database
PUT /customers/{user_id}/deactivate - deactivates a Customer record in the database
PUT /customers/{user_id}/activate - activates a Customer record in the database
"""

import os
import sys
import uuid
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from flask_restplus import Api, Resource, fields, reqparse, inputs
from werkzeug.exceptions import NotFound

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Customer, DataValidationError, Address

# Import Flask application
from . import app

# Document the type of autorization required
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Api-Key'
    }
}

######################################################################
# Configure Swagger before initilaizing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Customer REST API Service',
          description='This is a Customer server.',
          default='customers',
          default_label='Customers operations',
          # doc='/', 
          doc = '/apidocs/',
          authorizations=authorizations
          # prefix='/api'
         )


# Define the model so that the docs reflect what can be sent
customer_model = api.model('Customer', {
    'customer_id': fields.String(readOnly=True,
                         description='The unique id assigned internally by service'),
    'user_id': fields.String(required=True,
                         description='The unique id given by customer'),
    'first_name': fields.String(required=True,
                          description='The first name of the Customer'),
    'last_name': fields.String(required=True,
                              description='The last name of Customer (e.g., Wang, Gates, etc.)'),
    'password': fields.String(required=True,
                                description='Password'),
    'street': fields.String(required=True,
                                description='street'),
    'apartment': fields.String(required=True,
                                description='apartment'),
    'city': fields.String(required=True,
                                description='city'),
    'state': fields.String(required=True,
                                description='state'),
    'zip_code': fields.String(required=True,
                                description='zip_code'),
    'status': fields.String(required=False,
                                description='status'),
})

create_model = api.model('Customer', {
    'user_id': fields.String(required=True,
                         description='The unique id given by customer'),
    'first_name': fields.String(required=True,
                          description='The first name of the Customer'),
    'last_name': fields.String(required=True,
                              description='The last name of Customer (e.g., Wang, Gates, etc.)'),
    'password': fields.String(required=True,
                                description='Password'),
    'street': fields.String(required=True,
                                description='street'),
    'apartment': fields.String(required=True,
                                description='apartment'),
    'city': fields.String(required=True,
                                description='city'),
    'state': fields.String(required=True,
                                description='state'),
    'zip_code': fields.String(required=True,
                                description='zip_code')
})


######################################################################
# Authorization Decorator
######################################################################
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'X-Api-Key' in request.headers:
            token = request.headers['X-Api-Key']

        if app.config.get('API_KEY') and app.config['API_KEY'] == token:
            return f(*args, **kwargs)
        else:
            return {'message': 'Invalid or missing token'}, 401
    return decorated


######################################################################
# Function to generate a random API key (good for testing)
######################################################################
def generate_apikey():
    """ Helper function used when testing API keys """
    return uuid.uuid4().hex


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route('/healthcheck')
def healthcheck():
    """ Let them know our heart is still beating """
    return make_response(jsonify(status=200, message='Healthy'), status.HTTP_200_OK)

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)

@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_400_BAD_REQUEST,
                   error='Bad Request',
                   message=message), status.HTTP_400_BAD_REQUEST

@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_404_NOT_FOUND,
                   error='Not Found',
                   message=message), status.HTTP_404_NOT_FOUND

@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_405_METHOD_NOT_ALLOWED,
                   error='Method not Allowed',
                   message=message), status.HTTP_405_METHOD_NOT_ALLOWED

@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = str(error)
    app.logger.warning(message)
    return jsonify(status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                   error='Unsupported media type',
                   message=message), status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = str(error)
    app.logger.error(message)
    return jsonify(status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                   error='Internal Server Error',
                   message=message), status.HTTP_500_INTERNAL_SERVER_ERROR


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    return app.send_static_file('index.html')

######################################################################
# LIST ALL CUSTOMERS
######################################################################
@app.route('/customers', methods=['GET'])
def list_customers():
    """ Returns all of the Customers """
    app.logger.info('Request for customers list')
    customers = Customer.all()
    f_name = request.args.get('fname')
    l_name = request.args.get('lname')
    city = request.args.get('city')
    state = request.args.get('state')
    zip_code = request.args.get('zip')
    if f_name:
        customers = Customer.find_by_first_name(f_name)
    elif l_name:
        customers = Customer.find_by_last_name(l_name)
    elif city:
        customers = Address.find_by_city(city)
    elif state:
        customers = Address.find_by_state(state)
    elif zip_code:
        customers = Address.find_by_zip(zip_code)
    else:
        customers = Customer.all()
    results = [cust.serialize() for cust in customers]
    return make_response(jsonify(results), status.HTTP_200_OK)

######################################################################
# RETRIEVE A CUSTOMER
######################################################################
@app.route('/customers/<string:user_id>', methods=['GET'])
def get_customers(user_id):
    """
    Retrieve a single customer
    This endpoint will return a Customer based on user_id
    """
    app.logger.info('Request for customer with user_id: %s', user_id)
    cust = Customer.find(user_id)
    result = [customer.serialize() for customer in cust]
    if len(result) == 0:
        return make_response(jsonify(error="Customer not found"), status.HTTP_404_NOT_FOUND)
    return make_response(jsonify(result), status.HTTP_200_OK)

######################################################################
# ADD A NEW CUSTOMER
######################################################################
@app.route('/customers', methods=['POST'])
def create_customers():
    """
    Creates a Customer
    This endpoint will create a Customer based the data in the body that is posted
    """
    app.logger.info('Request to create a customer')
    check_content_type('application/json')
    data = request.get_json()

    cust = Customer()
    cust.deserialize(data)
    cust.save()
    customer_id = cust.customer_id
    addr = Address()
    addr.deserialize(data['address'])
    addr.customer_id = customer_id
    addr.save()
    cust.address_id = addr.id
    cust.save()
    message = cust.serialize()
    location_url = url_for('create_customers', customer_id=cust.customer_id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                             'Location': location_url
                         })


######################################################################
# DELETE A CUSTOMER
######################################################################
@app.route('/customers/<string:user_id>', methods=['DELETE'])
def delete_customers(user_id):

    """
    Delete a Customer
    This endpoint will delete a Customer based the id specified in the path
    """
    app.logger.info('Request to delete customer with user_id: %s', user_id)
    customer = Customer.find(user_id)
    if customer:
        cust = customer[0]
        cust.delete()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
# UPDATE A CUSTOMER
######################################################################
@app.route('/customers/<string:user_id>', methods=['PUT'])
def update_customers(user_id):
    """
    Update a Customer
    This endpoint will update a Customer based the body that is posted
    """
    app.logger.info('Request to update customer with id: %s', user_id)
    check_content_type('application/json')
    customers = Customer.find(user_id)
    if customers.count() == 0:
        raise NotFound("Customer with id '{}' was not found.".format(user_id))

    cust = customers[0]
    cust.deserialize(request.get_json())
    cust.user_id = user_id
    cust.save()
    return make_response(jsonify(cust.serialize()), status.HTTP_200_OK)

######################################################################
# DEACTIVATE A CUSTOMER
######################################################################
@app.route('/customers/<string:user_id>/deactivate', methods=['PUT'])
def deactivate_customers(user_id):
    """
    Deactivate a Customer
    This endpoint will deactivate a Customer
    """
    app.logger.info('Request to deactivate customer with id: %s', user_id)
    check_content_type('application/json')
    customers = Customer.find(user_id)
    if customers.count() == 0:
        raise NotFound("Customer with id '{}' was not found.".format(user_id))

    cust = customers[0]
    cust.user_id = user_id
    cust.active = False
    cust.save()
    return make_response(jsonify(cust.serialize()), status.HTTP_200_OK)

######################################################################
# ACTIVATE A CUSTOMER
######################################################################
@app.route('/customers/<string:user_id>/activate', methods=['PUT'])
def activate_customers(user_id):
    """
    Activate a Customer
    This endpoint will activate a Customer
    """
    app.logger.info('Request to activate customer with id: %s', user_id)
    check_content_type('application/json')
    customers = Customer.find(user_id, False)
    if customers.count() == 0:
        raise NotFound("Customer with id '{}' was not found.".format(user_id))

    cust = customers[0]
    cust.user_id = user_id
    cust.active = True
    cust.save()
    return make_response(jsonify(cust.serialize()), status.HTTP_200_OK)

######################################################################
# DELETE ALL CUSTOMER DATA (for testing only)
######################################################################
@app.route('/customers/reset', methods=['DELETE'])
def customers_reset():
    """ Removes all customers from the database """
    Customer.remove_all()
    init_db()
    return make_response('', status.HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Customer.init_db(app)
    Address.init_db(app)

def check_content_type(content_type):
    """ Checks that the media type is correct """
    if request.headers['Content-Type'] == content_type:
        return
    app.logger.error('Invalid Content-Type: %s', request.headers['Content-Type'])
    abort(415, 'Content-Type must be {}'.format(content_type))

def initialize_logging(log_level=logging.INFO):
    """ Initialized the default logging to STDOUT """
    if not app.debug:
        print('Setting up logging...')
        # Set up default logging for submodules to use STDOUT
        # datefmt='%m/%d/%Y %I:%M:%S %p'
        fmt = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
        logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)
        # Make a new log handler that uses STDOUT
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(fmt))
        handler.setLevel(log_level)
        # Remove the Flask default handlers and use our own
        handler_list = list(app.logger.handlers)
        for log_handler in handler_list:
            app.logger.removeHandler(log_handler)
        app.logger.addHandler(handler)
        app.logger.setLevel(log_level)
        app.logger.propagate = False
        app.logger.info('Logging handler established')
