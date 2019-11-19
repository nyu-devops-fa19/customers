Feature: The customer service back-end
    As a Customer Squad
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | user_id | first_name | last_name | password | street | apartment | city | state | zip_code |
        |   id1   |   fname1   |  lname1   |   pwd1   |  str1  |    apt1   | cty1 |  st1  |  code1   |
        |   id2   |   fname2   |  lname2   |   pwd2   |  str2  |    apt2   | cty2 |  st2  |  code2   |
        |   id3   |   fname3   |  lname3   |   pwd3   |  str3  |    apt3   | cty3 |  st3  |  code3   |
        |   id4   |   fname4   |  lname4   |   pwd4   |  str4  |    apt4   | cty3 |  st3  |  code4   |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: List all customers
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Retrieve" button
    Then I should see "fname1" in the results
    And I should see "fname2" in the results
    And I should see "fname3" in the results

Scenario: List all customers with first name fname1
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "first_name" to "fname1"
    And I press the "Retrieve" button
    Then I should see "fname1" in the results
    And I should not see "fname4" in the results

Scenario: List all customers with last name lname1
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "last_name" to "lname1"
    And I press the "Retrieve" button
    Then I should see "lname1" in the results
    And I should not see "lname4" in the results

Scenario: List all customers living in cty3
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "City" to "cty3"
    And I press the "Retrieve" button
    Then I should see "fname3" in the results
    And I should see "fname4" in the results
    And I should not see "fname1" in the results

Scenario: List all customers living in state st3
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "State" to "st3"
    And I press the "Retrieve" button
    Then I should see "fname3" in the results
    And I should see "fname4" in the results
    And I should not see "fname2" in the results

Scenario: List all customers with zip code code2
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "zip_code" to "code2"
    And I press the "Retrieve" button
    Then I should see "fname2" in the results
    And I should not see "fname3" in the results

Scenario: Deactivate a Customer
    When I visit the "Home Page"
    And I set the "user_id" to "id1"
    And I press the "Deactivate" button
    Then I should see the message "Customer deactivated."
    Then I should not see "true" in the results

Scenario: Create a Customer
    When I visit the "Home Page"
    And I set the "user_id" to "merrywang"
    And I set the "first_name" to "merry"
    And I set the "last_name" to "wang"
    And I set the "password" to "password123"
    And I set the "street" to "100 w"
    And I set the "apartment" to "233"
    And I set the "city" to "new york city"
    And I set the "state" to "new york state"
    And I set the "zip_code" to "10022"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "user_id" field
    And I press the "Clear" button
    Then the "user_id" field should be empty
    And the "first_name" field should be empty
    And the "last_name" field should be empty
    And the "password" field should be empty
    And the "street" field should be empty
    And the "apartment" field should be empty
    And the "city" field should be empty
    And the "state" field should be empty
    And the "zip_code" field should be empty
    When I paste the "user_id" field
    And I press the "search" button
    Then I should see "merrywang" in the "user_id" field
    Then I should see "merry" in the "first_name" field
    Then I should see "wang" in the "last_name" field
    Then I should see "100 w" in the "street" field
    Then I should see "233" in the "apartment" field
    Then I should see "new york city" in the "city" field
    Then I should see "new york state" in the "state" field
    Then I should see "10022" in the "zip_code" field
