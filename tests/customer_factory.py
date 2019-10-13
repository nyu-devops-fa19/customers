# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test Factory to make fake objects for testing
"""
import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger
from service.models import Customer

class CustomerFactory(factory.Factory):
    """ Creates fake customers that you don't have to feed """
    class Meta:
        model = Customer
    id = factory.Sequence(lambda n: n)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    address = factory.Faker('address')
    customer_id = FuzzyInteger(1,100) # Assume that the customer_id is from 1 to 100
    user_id = FuzzyText(8) # Assume that the length of user_id is 8
    password = FuzzyText(8) # Assume that the length of password is 8
    available = FuzzyChoice(choices=[True, False])

if __name__ == '__main__':
    for _ in range(10):
        customer = CustomerFactory()
        print(customer.serialize())
