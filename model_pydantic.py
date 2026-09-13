from pydantic import BaseModel, EmailStr, field_validator, model_validator
import json


class Address(BaseModel):
    city: str
    street: str
    house_number: int

    @field_validator("city")
    @classmethod
    def validate_city(cls, value):
        if len(value) < 2:
            raise ValueError("City must contain at least 2 characters")
        return value

    @field_validator("street")
    @classmethod
    def validate_street(cls, value):
        if len(value) < 3:
            raise ValueError("Street must contain at least 3 characters")
        return value

    @field_validator("house_number")
    @classmethod
    def validate_house_number(cls, value):
        if value <= 0:
            raise ValueError("House number must be positive")
        return value


class User(BaseModel):
    name: str
    age: int
    email: EmailStr
    is_employed: bool
    address: Address

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if len(value) < 2:
            raise ValueError("Name must contain at least 2 characters")

        if not value.isalpha():
            raise ValueError("Name must contain only letters")

        return value

    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if value < 0 or value > 120:
            raise ValueError("Age must be between 0 and 120")

        return value

    @model_validator(mode="after")
    def validate_employment_age(self):
        if self.is_employed:
            if self.age < 18 or self.age > 65:
                raise ValueError(
                    "Employed user must be between 18 and 65 years old"
                )

        return self


def process_user_json(json_input):
    try:
        data = json.loads(json_input)

        user = User(**data)

        return user.model_dump_json(indent=4)

    except Exception as error:
        return f"Validation error: {error}"


# Successful example

json_input = """
{
    "name": "John",
    "age": 30,
    "email": "john.doe@example.com",
    "is_employed": true,
    "address": {
        "city": "Berlin",
        "street": "Main Street",
        "house_number": 10
    }
}
"""

print("Successful registration:")
print(process_user_json(json_input))


# Error: employed user is younger than 18

json_input_error_age = """
{
    "name": "Tom",
    "age": 16,
    "email": "tom@example.com",
    "is_employed": true,
    "address": {
        "city": "Berlin",
        "street": "Main Street",
        "house_number": 10
    }
}
"""

print("\nError example - age:")
print(process_user_json(json_input_error_age))


# Error: invalid house number

json_input_error_house = """
{
    "name": "Anna",
    "age": 25,
    "email": "anna@example.com",
    "is_employed": false,
    "address": {
        "city": "Berlin",
        "street": "Main Street",
        "house_number": -5
    }
}
"""

print("\nError example - house number:")
print(process_user_json(json_input_error_house))