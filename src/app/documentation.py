from pydantic import field_validator, BaseModel


class PhoneAddressSchema(BaseModel):
    phone: str
    address: str

    @field_validator('phone', mode='before')
    @classmethod
    def check_phone(cls, value: str):
        if not value.startswith("+7"):
            raise ValueError(f"{value} is not a russian number format")
        if len(value) != 12:
            raise ValueError(f"{value} has incorrect length")

        return value


class AddressUpdateSchema(BaseModel):
    address: str
