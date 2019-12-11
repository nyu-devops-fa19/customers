[![Build Status](https://travis-ci.org/nyu-devops-fa19/customers.svg?branch=master)](https://travis-ci.org/nyu-devops-fa19/customers)
[![codecov](https://codecov.io/gh/nyu-devops-fa19/customers/branch/master/graph/badge.svg)](https://codecov.io/gh/nyu-devops-fa19/customers)

# Customers

## Description
customer squads of a e-commerce website

## Service, pipeline URLs
- Prod: https://nyu-customer-service-f19.mybluemix.net/
- Dev: https://nyu-customer-service-f19-dev.mybluemix.net/
- Pipeline: https://cloud.ibm.com/devops/pipelines/a53e9506-a90e-46c8-b92c-42a4ca964834?env_id=ibm:yp:us-south
- API Doc: https://nyu-customer-service-f19.mybluemix.net/apidocs

## PostgreSQL(from ElephantSQL.com)
- URL (dev): `postgres://ramcqzam:F-i4xNnzQIwhXAef134Bfus0oBI5bl-m@rajje.db.elephantsql.com:5432/ramcqzam`
- URL (prod): `postgres://grtjewnq:Bq2G7mAUIIU3c07CMbXZg2l0n6xLRLAp@rajje.db.elephantsql.com:5432/grtjewnq`

## To run the Flask app locally

```
vagrant up
vagrant ssh
cd /vagrant/
honcho start
```
Then on your own machine, you can see by visiting: http://localhost:5000/

## Running the tests
- Unit tests (after `cd /vagrant/`): `nosetests`
- Integration tests (after `cd /vagrant/` and `honcho start`): `behave`

## APIs routes
#### **Create** 
- **POST** `/customers`  
Body: JSON containing following fields
  * first_name - String  
  * last_name - String  
  * user_id - String  
  * password - String (at least 6 characters long)
  * address - JSON containing:  
    * street - String  
    * apartment - String   
    * city - String  
    * state - String  
    * zip_code - String

  Example:  
```
{
    "first_name": "John",
    "last_name": "Doe",
    "user_id": "jhd345",
    "password": "Asdf@1234",
    "address": {
        "street": "48 John St",
        "apartment": "1B",
        "city": "New York",
        "state": "New York",
        "zip_code": "22890"
    }
}
```

#### **Read** 
- **GET** `/customers/{user_id}`

#### **Update**
- **PUT** `/customers/{user_id}`

#### **Delete**
- **DELETE** `/customers/{user_id}`

#### **List**
- **GET** `/customers`

#### **Query**
- **GET** `/customers?param={value}`  
Choices of param:
  * fname - first name (String)  
  * lname - last name (String)  
  * city - city of primary address (String)  
  * state - state of primary address (String)  
  * zip_code - zip code of primary address (String)  

#### **Deactivate**
- **PUT** `/customers/{user_id}/deactivate`

#### **Activate**
- **PUT** `/customers/{user_id}/activate`
