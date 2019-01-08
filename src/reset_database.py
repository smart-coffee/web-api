import time
import datetime

from models import DB, User, Role, CoffeeMachine, CoffeeType, CoffeeBrand, CoffeeProduct, Profile, Job


def reset_database():
    DB.drop_all()
    DB.create_all()

    role = Role()
    role.name = 'Administrator'

    user = User()
    user.public_id = 'd38924fb-9417-4a50-b715-01f805c28063'
    user.password = 'sha256$PaWEzGH9$7ee9e7ea744fb7c10d9332b21d8d0c0e611aa37dac9e2b493a658aaa07168b25'
    user.name = 'admin'
    user.email = 'some.email@domain.tld'
    user.role = role

    coffee_machine = CoffeeMachine()
    coffee_machine.name = 'Winston'
    coffee_machine.repository = 'hidden-firefly'

    coffee_type = CoffeeType()
    coffee_type.name = 'Arabica'

    coffee_brand = CoffeeBrand()
    coffee_brand.name = 'Dallmayr'

    coffee_product = CoffeeProduct()
    coffee_product.name = 'Dallmayr Prodomo'
    coffee_product.coffee_brand = coffee_brand
    coffee_product.coffee_type = coffee_type

    profile = Profile()
    profile.name = 'Morning'
    profile.water_in_percent = 32 * 1000
    profile.coffee_strength_in_percent = 42
    profile.user = user

    job = Job()
    current_time = time.time()
    job.create_date = current_time
    job.coffee_strength_in_percent = 66
    job.water_in_percent = 44
    job.price = 10
    job.doses = 1
    job.user = user
    job.coffee_machine = coffee_machine
    job.coffee_product = coffee_product


    DB.session.add(job)
    DB.session.commit()


reset_database()
