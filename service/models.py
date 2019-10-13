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
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'), nullable=True)

    def serialize(self):
        """ Serializes an Address into a dictionary """
        return {"id": self.id,
                "street": self.street,
                "apartment": self.apartment,
                "city": self.city,
                "state": self.state,
                "zip code": self.zip_code}

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
        except TypeError as error:
            raise DataValidationError('Invalid address: body of request contained' \
                                      'bad or no data')
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

    __table_args__ = (
        CheckConstraint('char_length(password) > 5',
                        name='password_min_length'),
    )

    @validates('password')
    def validate_password(self, key, password) -> str:
        if len(password) <= 5:
            raise ValueError('password too short')
        return password

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        return {"id": self.customer_id,
                "first name": self.first_name,
                "last name": self.last_name,
                "user id": self.user_id,
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
            raise DataValidationError('Invalid pet: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid pet: body of request contained' \
                'bad or no data')
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
    '''
    TODO: Add methods for save, delete, list and query operations here

    def delete(self):
        """ Removes a Pet from the data store """
        Pet.logger.info('Deleting %s', self.name)
        db.session.delete(self)
        db.session.commit()
    '''
    @classmethod
    def find(cls, user_id):
        """ Finds a Pet by it's ID """
        cls.logger.info('Processing lookup for id %s ...', user_id)
        return cls.query.filter(cls.user_id == user_id)
    '''
    @classmethod
    def find_or_404(cls, pet_id):
        """ Find a Pet by it's id """
        cls.logger.info('Processing lookup or 404 for id %s ...', pet_id)
        return cls.query.get_or_404(pet_id)

    @classmethod
    def find_by_name(cls, name):
        """ Returns all Pets with the given name

        Args:
            name (string): the name of the Pets you want to match
        """
        cls.logger.info('Processing name query for %s ...', name)
        return cls.query.filter(cls.name == name)

    @classmethod
    def find_by_category(cls, category):
        """ Returns all of the Pets in a category

        Args:
            category (string): the category of the Pets you want to match
        """
        cls.logger.info('Processing category query for %s ...', category)
        return cls.query.filter(cls.category == category)

    @classmethod
    def find_by_availability(cls, available=True):
        """ Query that finds Pets by their availability """
        """ Returns all Pets by their availability

        Args:
            available (boolean): True for pets that are available
        """
        cls.logger.info('Processing available query for %s ...', available)
        return cls.query.filter(cls.available == available)
    '''