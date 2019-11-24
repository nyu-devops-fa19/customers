"""
Models for Customers module

All of the models are stored in this module

Models
------
Customer - A user of the eCommerce website

Attributes:
-----------
customer_id (string) - ID of the customer, generated by the database, unique
first_name (string) - the first name of the customer
last_name (string) - the last name of the customer
user_id (string) - User ID of the customer, unique, chosen by the customer at the time of registration
password (string) - Password of the customer, used for logging in
address_id(int) - id of the customer's primary address
"""

import logging
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import validates

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass

class Address(db.Model):

    logger = logging.getLogger('flask.app')
    app = None

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String)
    apartment = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip_code = db.Column(db.String)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=False)

    def serialize(self):
        """ Serializes an Address into a dictionary """
        return {"id": self.id,
                "street": self.street,
                "apartment": self.apartment,
                "city": self.city,
                "state": self.state,
                "zip_code": self.zip_code}

    def deserialize(self, data):
        """
        Deserializes an Address from a dictionary

        Args:
            data (dict): A dictionary containing the Address data
        """
        try:
            self.street = data['street']
            self.apartment = data['apartment']
            self.city = data['city']
            self.state = data['state']
            self.zip_code = data['zip_code']
        except KeyError as error:
            raise DataValidationError('Invalid address: missing ' + error.args[0])
        return self

    def save(self):
        """
        Saves an Address to the data store
        """
        Address.logger.info('Saving %s %s', self.street, self.apartment)
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """ Initializes the database sesssion """
        cls.logger.info('Initializing database')
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tabless

    @classmethod
    def find_by_city(cls, city):
        """ Returns all addresses in the given city

        Args:
            city (string): the city of the Addresses you want to match
        """
        cls.logger.info('Processing city query for %s ...', city)
        addresses = cls.query.filter(cls.city == city)
        return [Customer.find_by_cust_id(addr.customer_id) for addr in addresses]

    @classmethod
    def find_by_state(cls, state):
        """ Returns all addresses in the given state

        Args:
            state (string): the state of the Addresses you want to match
        """
        cls.logger.info('Processing state query for %s ...', state)
        addresses = cls.query.filter(cls.state == state)
        return [Customer.find_by_cust_id(addr.customer_id) for addr in addresses]

    @classmethod
    def find_by_zip(cls, zip_code):
        """ Returns all addresses in the given zip code

        Args:
            zip_code (string): the zip_code of the Customers you want to match
        """
        cls.logger.info('Processing zip query for %s ...', zip_code)
        addresses = cls.query.filter(cls.zip_code == zip_code)
        return [Customer.find_by_cust_id(addr.customer_id) for addr in addresses]

    @classmethod
    def find(cls, addr_id):
        """ Finds an address by its ID """
        cls.logger.info('Processing lookup for id %s ...', addr_id)
        return cls.query.get(addr_id).serialize()

    @classmethod
    def all(cls):
        """ Returns all of the Addresses in the database """
        cls.logger.info('Processing all Addresses')
        return cls.query.all()

    @classmethod
    def delete(cls, addr_id):
        """ Removes a Address from the data store """
        cls.logger.info('Deleting %s', addr_id)
        db.session.delete(cls.query.get(addr_id))
        db.session.commit()

    @classmethod
    def remove_all(cls):
        """ Removes all products from the database (use for testing)  """
        for address in cls.query.all():
            db.session.delete(address)
        db.session.commit()

class Customer(db.Model):
    """
    Class that represents a Customer
    """
    __tablename__ = 'customer'
    logger = logging.getLogger('flask.app')
    app = None

    # Table Schema
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    address_id = db.Column(db.Integer, nullable=True)

    # __table_args__ = (
    #     CheckConstraint('char_length(password) > 5',
    #                     name='password_min_length'),
    # )

    # @validates('password')
    # def validate_password(self, key, password) -> str:
    #     if len(password) <= 5:
    #         raise ValueError('password too short')
    #     return password

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        return {"customer_id": self.customer_id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "user_id": self.user_id,
                "active": self.active,
                "address": Address.find(self.address_id)}

    def internal_serialize(self):
        """ Internal_serializes a Customer into a dictionary """
        return {"first_name": self.first_name,
                "last_name": self.last_name,
                "user_id": self.user_id,
                "password": self.password,
                "active": self.active}

    def deserialize(self, data):
        """
        Deserializes a Customer from a dictionary

        Args:
            data (dict): A dictionary containing the Customer data
        """
        try:
            self.first_name = data['first_name']
            self.last_name = data['last_name']
            self.user_id = data['user_id']
            self.password = data['password']
            self.active = True
        except KeyError as error:
            raise DataValidationError('Invalid customer: missing ' + error.args[0])
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database sesssion """
        cls.logger.info('Initializing database')
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    def save(self):
        """
        Saves a Customer to the data store
        """
        Customer.logger.info('Saving %s %s', self.first_name, self.last_name)
        if not self.customer_id:
            db.session.add(self)
        db.session.commit()

    @classmethod
    def all(cls):
        """ Returns all of the Customers in the database """
        cls.logger.info('Processing all Customers')
        return cls.query.all()

    @classmethod
    def remove_all(cls):
        """ Removes all products from the database (use for testing)  """
        for customer in cls.query.all():
            db.session.delete(customer)
        db.session.commit()

    @classmethod
    def find_by_first_name(cls, f_name):
        """ Returns all of the Customers with the given first name

        Args:
            f_name (string): the first name of the Customers you want to match
        """
        cls.logger.info('Processing first name query for %s ...', f_name)
        return cls.query.filter(cls.first_name == f_name)

    @classmethod
    def find_by_last_name(cls, l_name):
        """ Returns all of the Customers with the given last name

        Args:
            l_name (string): the first name of the Customers you want to match
        """
        cls.logger.info('Processing last name query for %s ...', l_name)
        return cls.query.filter(cls.last_name == l_name)

    @classmethod
    def find_by_cust_id(cls, cust_id):
        """ Finds a Customer by it's customer ID """
        cls.logger.info('Processing lookup for customer_id %s ...', cust_id)
        active_customers = cls.query.filter(cls.customer_id == cust_id and cls.active)
        return active_customers[0]

    def delete(self):
        """ Removes a Customer from the data store """
        Customer.logger.info('Deleting %s %s', self.first_name, self.last_name)
        Address.delete(self.address_id)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find(cls, user_id, filter_activate = True):
        """ Finds a Customer by user_id """
        cls.logger.info('Processing lookup for id %s ...', user_id)
        if filter_activate:
            return cls.query.filter(cls.user_id == user_id and cls.active)
        else:
            return cls.query.filter(cls.user_id == user_id)
    '''
    @classmethod
    def find_or_404(cls, pet_id):
        """ Find a Pet by it's id """
        cls.logger.info('Processing lookup or 404 for id %s ...', pet_id)
        return cls.query.get_or_404(pet_id)
    '''
