from pydantic import BaseModel,Field,field_validator,model_validator

#pip install pydantic
class User(BaseModel):
    id: int
    name: str
    age: int = Field(gt=0, lt=120)

user = User(id="1", name="Alice", age=20)
print(user)

#If you want strict validation

# class User(BaseModel):
#     id: StrictInt
#     name: str
#     age: int = Field(gt=0, lt=120)

#Handling Default Values and Required Fields
class UserProfile(BaseModel):
    name: str
    age: int = 43
    email: str
    is_active: bool = True

user = UserProfile(name="Sofia Moretti", email="sofia.moretti@example.com")
print(user)

#Advanced Validation Techniques

#1.Field Validators (@field_validator)--define custom validation rules for individual fields. 

class UserProfile(BaseModel):
    name: str
    age: int
    email: str

    @field_validator('age')
    def check_age(cls, value):
        if value < 18:
            raise ValueError('Age must be at least 18')
        return value

x=UserProfile(name="Noah Müller", age=20, email="noah.muller@example.com")
print(x)

#2.Validators for Entire Model--define validation rules that involve multiple fields or the model as a whole.
class User(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def check_passwords(self):   # 👈 NO @classmethod, no cls
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

User(password="a", confirm_password="a")

#3.Nested Models and Complex Data Structures
class Address(BaseModel):
    street: str
    city: str

class UserProfile(BaseModel):
    name: str
    age: int
    email: str
    address: Address

address = Address(street="10 Rue de la Paix", city="Paris")
user = UserProfile(name="Emma Dubois", age=34, email="emma.dubois@example.fr", address=address)
print(user)




