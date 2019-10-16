# Customers

## Description
customer squads of a e-commerce website

## To run the Flask app 

```
vagrant up
vagrant ssh
cd /vagrant
nosetests
FLASK_APP=service:app flask run --host=0.0.0.0 --port=5000
```
Then on your own machine, you can see by visiting: http://localhost:5000/

## APIs routes
- **Create** 
* POST /customers  
Body: JSON containing the following fields:  
first_name - String  
last_name - String  
user_id - String  
password - String(at least 6 characters long) . 
address - JSON containing:  
	street - String  
	apartment - String   
	city - String  
	state - String  
	zip_code - String  
For example:  
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

- **Read** 
* GET /customers/user_id  
    
- **Update**
* PUT /customers/user_id
  
- **Delete**
* DELETE /customers/user_id
  
- **List**
* GET /customers

- **Query**
* GET /customers?param={value}
Where param could be either of the following:  
fname - first name (String)  
lname - last name (String)  
uid - user id (String)  
city - city of primary address (String)  
state - state of primary address (String)  
zip - zip code of primary address (String)  
  
- **Deactivate**
* PUT /customers/user_id/deactivate

- **Activate**
* PUT /customers/user_id/activate

## Running the tests
Run the tests using `nose`  
`nosetests`  
The code coverage tool in `nose` directly give the report:  
`coverage report -m`