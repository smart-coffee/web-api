from config.flask_config import ResourceNotFound
from models import User, Role, CoffeeMachine, CoffeeType, CoffeeBrand, CoffeeProduct


def run_user_fixture(user: User):
    pass

def run_role_fixture(role: Role):
    pass

def run_coffee_machine_fixture(coffee_machine: CoffeeMachine):
    pass

def run_coffee_type_fixture(coffee_type: CoffeeType):
    pass

def run_coffee_brand_fixture(coffee_brand: CoffeeBrand):
    pass

def run_coffee_product_fixture(coffee_product: CoffeeProduct):
    coffee_product.coffee_brand_id = coffee_product.coffee_brand_id_fk
    coffee_product.coffee_type_id = coffee_product.coffee_type_id_fk