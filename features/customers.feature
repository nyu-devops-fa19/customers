Feature: The customer service back-end
    As a Customer Squad
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
        | user_id | first_name | last_name | password | street | apartment | city | state | zip_code |
        |   id1   |   fname1   |  lname1   |   pwd1   |  st1   |    apt1   | cty1 |  st1  |  code1   |
        |   id2   |   fname2   |  lname2   |   pwd2   |  st2   |    apt2   | cty2 |  st2  |  code2   |
        |   id3   |   fname3   |  lname3   |   pwd3   |  st3   |    apt3   | cty3 |  st3  |  code3   |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Deactivate a Customer
    When I visit the "Home Page"
    And I set the "user_id" to "id1"
    And I press the "Deactivate" button
    Then I should see the message "Customer deactivated."
    Then I should not see "true" in the results

Scenario: Update a Customer
    When I visit the "Home Page"
    And I set the "user_id" to "id1"
    And I press the "search" button
    Then I should see "fname1" in the "first_name" field
    And I should see "lname1" in the "last_name" field
    And I should see "st1" in the "street" field
    And I should see "apt1" in the "apartment" field
    And I should see "cty1" in the "city" field
    And I should see "st1" in the "state" field
    And I should see "code1" in the "zip_code" field
    When I change "first_name" to "fchanged_name"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "user_id" field
    And I press the "Clear" button
    And I paste the "user_id" field
    And I press the "Search" button
    Then I should see "fchanged_name" in the "first_name" field
    When I copy the "first_name" field
    And I press the "Clear" button
    And I paste the "first_name" field
    And I press the "Retrieve" button
    Then I should see "fchanged_name" in the results
    Then I should not see "fname1" in the results


Scenario: Delete a Customer
    When I visit the "Home Page"
    And I set the "user_id" to "id1"
    And I press the "Delete" button
    Then I should see the message "Customer has been Deleted!"


