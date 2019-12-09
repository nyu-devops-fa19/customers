[![Build Status](https://travis-ci.org/nyu-devops-fa19/customers.svg?branch=master)](https://travis-ci.org/nyu-devops-fa19/customers)
[![codecov](https://codecov.io/gh/nyu-devops-fa19/customers/branch/master/graph/badge.svg)](https://codecov.io/gh/nyu-devops-fa19/customers)

# Customers

## Description
customer squads of a e-commerce website

## PostgreSQL(from ElephantSQL.com)
Name: `yazjsysy`  
Password: `vuMLNAWJTu1VlMof3Z-c2KU1W_jp8dab`  
URL: `postgres://yazjsysy:vuMLNAWJTu1VlMof3Z-c2KU1W_jp8dab@salt.db.elephantsql.com:5432/yazjsysy`  
API Key: `aafb0461-29be-4699-bac2-d1017ae79cf9`

## To run the Flask app 

```
vagrant up
vagrant ssh
cd /vagrant/
honcho start
```
Then on your own machine, you can see by visiting: http://localhost:5000/

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

## Running the tests
Run the tests using `nose`  
`nosetests`

## Dev

## Prod

## Pipeline
