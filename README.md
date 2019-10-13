customer squads of a e-commerce website

APIs:
1. Create:
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

2. Read:
* GET /customers/<id>  
  <id> is the customer_id
    
3. Update:
* PUT /customers/<id>
  
4. Delete:
* DELETE /customers/<id>
  
5. List:
* GET /customers

6. Query:
* GET /customers?param={value}
Where param could be either of the following:  
fname - first name (String)  
lname - last name (String)  
uid - user id (String)  
city - city of primary address (String)  
state - state of primary address (String)  
zip - zip code of primary address (String)  
  
7. Deactivate:
* PUT /customers/<id>
