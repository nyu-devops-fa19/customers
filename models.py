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
primary_address(string) - primary address of the customer
addresses (List(string)) - contains at least one address for every customer
"""

import logging
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    pass


class Customer(db.model):
    """
    Class that represents a Customer
    """
    __tablename__ = 'customer'
    logger = logging.getLogger('flask.app')
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    primary_address = db.Column(db.String(100), nullable=False)
    addresses = relationship("Child")

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        return {"id": self.id,
                "first name": self.first_name,
                "last name": self.last_name,
                "user id": self.user_id,
                "primary address": self.primary_address,
                "addresses": self.addresses}

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
            self.primary_address = data['primary_address']
            self.addresses = data['addresses']
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

            '''
            TODO: Add methods for save, delete, list and query operations here

            def save(self):
                """
                Saves a Pet to the data store
                """
                Pet.logger.info('Saving %s', self.name)
                if not self.id:
                    db.session.add(self)
                db.session.commit()

            def delete(self):
                """ Removes a Pet from the data store """
                Pet.logger.info('Deleting %s', self.name)
                db.session.delete(self)
                db.session.commit()

            @classmethod
            def all(cls):
                """ Returns all of the Pets in the database """
                cls.logger.info('Processing all Pets')
                return cls.query.all()

            @classmethod
            def find(cls, pet_id):
                """ Finds a Pet by it's ID """
                cls.logger.info('Processing lookup for id %s ...', pet_id)
                return cls.query.get(pet_id)

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


class Address(db.model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    customer = relationship("Parent", back_populates="addresses")
    address = db.Column(db.String(100))