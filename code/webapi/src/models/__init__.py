from config import DB
import enum


class User(DB.Model):
	__tablename__ = 'user'
	id = DB.Column(DB.Integer, primary_key=True)
	
	# Attributes
	public_id = DB.Column(DB.String(150), unique=True, nullable=False)
	name = DB.Column(DB.String(30), unique=True, nullable=False)
	password = DB.Column(DB.String(150), nullable=False)
	email = DB.Column(DB.String(50), nullable=False)
	
	# Foreign Keys
	role_id_fk = DB.Column(DB.Integer, DB.ForeignKey('role.id', name='fk_user_role'), nullable=False)
	
	# Relationships: 1 .. n
	profiles = DB.relationship('Profile', back_populates='user')
	jobs = DB.relationship('Job', back_populates='user')
	
	# Relationships: n .. 1
	role = DB.relationship('Role', foreign_keys=[role_id_fk], back_populates='users')

	def get_id(self):
		return self.id
		
		
class Role(DB.Model):
	__tablename__ = 'role'
	id = DB.Column(DB.Integer, primary_key=True)
	
	# Attributes
	name = DB.Column(DB.String(30), unique=True, nullable=False)
	
	# Relationships: 1 .. n
	users = DB.relationship('User', back_populates='role')
	
	def get_id(self):
		return self.id
		
		
class Profile(DB.Model):
	__tablename__ = 'profile'
	id = DB.Column(DB.Integer, primary_key=True)
	
	# Attributes
	name = DB.Column(DB.String(30), unique=True, nullable=False)
	coffee_strength_in_percent = DB.Column(DB.Integer, nullable=False)
	water_in_percent = DB.Column(DB.Integer, nullable=False)

	# Foreign Keys
	user_id_fk = DB.Column(DB.Integer, DB.ForeignKey('user.id', name='fk_profile_user'), nullable=False)
	
	# Relationships: n .. 1
	user = DB.relationship('User', foreign_keys=[user_id_fk], back_populates='profiles')

	def get_id(self):
		return self.id
		
		
class CoffeeBrand(DB.Model):
	__tablename__ = 'coffeebrand'
	id = DB.Column(DB.Integer, primary_key=True)
	
	# Attributes
	name = DB.Column(DB.String(30), unique=True, nullable=False)
	
	# Relationships: 1 .. n
	products = DB.relationship('CoffeeProduct', back_populates='coffee_brand')
	
	def get_id(self):
		return self.id
		
		
class CoffeeType(DB.Model):
	__tablename__ = 'coffeetype'
	id = DB.Column(DB.Integer, primary_key=True)
	
	# Attributes
	name = DB.Column(DB.String(30), unique=True, nullable=False)
	
	# Relationships: 1 .. n
	products = DB.relationship('CoffeeProduct', back_populates='coffee_type')
	
	def get_id(self):
		return self.id
		
		
class CoffeeProduct(DB.Model):
	__tablename__ = 'coffeeproduct'
	id = DB.Column(DB.Integer, primary_key=True)
	
	# Attributes
	name = DB.Column(DB.String(50), unique=True, nullable=False)

	# Foreign Keys
	coffee_type_id_fk = DB.Column(DB.Integer, DB.ForeignKey('coffeetype.id', name='fk_coffeeproduct_coffee_type'))
	coffee_brand_id_fk = DB.Column(DB.Integer, DB.ForeignKey('coffeebrand.id', name='fk_coffeeproduct_coffee_brand'))
	
	# Relationships: 1 .. n
	jobs = DB.relationship('Job', back_populates='coffee_product')
	
	# Relationships: n .. 1
	coffee_type = DB.relationship('CoffeeType', foreign_keys=[coffee_type_id_fk], back_populates='products')
	coffee_brand = DB.relationship('CoffeeBrand', foreign_keys=[coffee_brand_id_fk], back_populates='products')

	def get_id(self):
		return self.id
		
		
class CoffeeMachine(DB.Model):
	__tablename__ = 'coffeemachine'
	id = DB.Column(DB.Integer, primary_key=True)
	
	# Attributes
	name = DB.Column(DB.String(50), unique=True, nullable=False)
	
	# Relationships: 1 .. n
	jobs = DB.relationship('Job', back_populates='coffee_machine')
	
	def get_id(self):
		return self.id
		
		
class Job(DB.Model):
	__tablename__ = 'job'
	id = DB.Column(DB.Integer, primary_key=True)
	
	# Attributes
	create_date = DB.Column(DB.Integer, nullable=False)
	square_date = DB.Column(DB.Integer)
	coffee_strength_in_percent = DB.Column(DB.Integer, nullable=False)
	water_in_percent = DB.Column(DB.Integer, nullable=False)
	price = DB.Column(DB.Integer, nullable=False)
	doeses = DB.Column(DB.Integer, nullable=False)
	
	# Foreign Keys
	coffee_machine_id_fk = DB.Column(DB.Integer, DB.ForeignKey('coffeemachine.id', name='fk_job_coffee_machine'), nullable=False)
	coffee_product_id_fk = DB.Column(DB.Integer, DB.ForeignKey('coffeeproduct.id', name='fk_job_coffee_product'), nullable=False)
	user_id_fk = DB.Column(DB.Integer, DB.ForeignKey('user.id', name='fk_job_user'), nullable=False)
	
	# Relationships: n .. 1
	user = DB.relationship('User', foreign_keys=[user_id_fk], back_populates='jobs')
	coffee_machine = DB.relationship('CoffeeMachine', foreign_keys=[coffee_machine_id_fk], back_populates='jobs')
	coffee_product = DB.relationship('CoffeeProduct', foreign_keys=[coffee_product_id_fk], back_populates='jobs')

	def get_id(self):
		return self.id