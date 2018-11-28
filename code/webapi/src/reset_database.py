from models import DB, User, Role, CoffeeMachine, CoffeeType


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

    DB.session.add(user)
    DB.session.add(coffee_machine)
    DB.session.add(coffee_type)
    DB.session.commit()


reset_database()
