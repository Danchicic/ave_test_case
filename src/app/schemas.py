from typing import TypedDict


class PhoneAddressResponse(TypedDict):
    phone: str
    address: str


class AddressUpdateResponse(TypedDict):
    address: str
