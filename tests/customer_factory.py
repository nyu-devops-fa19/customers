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
import string
import random
from factory.fuzzy import FuzzyChoice, FuzzyInteger, FuzzyText
from service.models import Customer

class AddressFactory(factory.Factory):
    id = factory.Sequence(lambda n: n)

    street = FuzzyText(random.randint(1,20), chars=string.ascii_letters + string.digits)
    apartment = FuzzyText(random.randint(1,20), chars=string.ascii_letters + string.digits)
    city = FuzzyText(random.randint(1,20), chars=string.ascii_letters + string.digits)
    state = FuzzyText(random.randint(1,20), chars=string.ascii_letters + string.digits)
    zip_code = FuzzyText(5, chars=string.digits)
    customer_id = factory.Sequence(lambda n: n)



class CustomerFactory(factory.Factory):
    """ Creates fake customers that you don't have to feed """
    class Meta:
        model = Customer
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    Address = AddressFactory()

    user_id = FuzzyText(random.randint(1,20), chars=string.ascii_letters + string.digits) # Assume that the length of user_id is 8
    password = FuzzyText(random.randint(1,20), chars=string.ascii_letters + string.digits) # Assume that the length of password is 8
    active = FuzzyChoice(choices=[True, False])

if __name__ == '__main__':
    for _ in range(10):
        customer = CustomerFactory()
        print(customer.serialize())
