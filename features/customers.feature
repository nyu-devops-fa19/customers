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


# Scenario: The server is running
#     When I visited the "Homw Page"
#     Then I should see
