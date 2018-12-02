from config.flask_config import ResourceNotFound
from models import User, Role, CoffeeMachine, CoffeeType, CoffeeBrand, CoffeeProduct, Profile, Job


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

def run_profile_fixture(profile: Profile):
    user = User.query.filter_by(id=profile.user_id_fk).first()
    profile.user_id = user.public_id

def run_job_fixture(job: Job):
    job.coffee_machine_id = job.coffee_machine_id_fk
    job.coffee_product_id = job.coffee_product_id_fk
    user = User.query.filter_by(id=job.user_id_fk).first()
    job.user_id = user.public_id