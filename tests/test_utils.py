from types import SimpleNamespace

import pytest

from api.utils import marshal, unmarshal


def test_unmarshal():
    json_data = {
        "name": "John",
        "age": 30,
        "address": {"city": "New York", "zipcode": "10001"},
        "contacts": [
            {"type": "phone", "number": "123-4567"},
            {"type": "email", "address": "john@example.com"},
        ],
    }
    namespace_obj = unmarshal(json_data)

    assert isinstance(namespace_obj, SimpleNamespace)
    assert namespace_obj.name == "John"
    assert namespace_obj.age == 30
    assert isinstance(namespace_obj.address, SimpleNamespace)
    assert namespace_obj.address.city == "New York"
    assert namespace_obj.address.zipcode == "10001"
    assert isinstance(namespace_obj.contacts, list)
    assert isinstance(namespace_obj.contacts[0], SimpleNamespace)
    assert namespace_obj.contacts[0].type == "phone"
    assert namespace_obj.contacts[0].number == "123-4567"
    assert namespace_obj.contacts[1].type == "email"
    assert namespace_obj.contacts[1].address == "john@example.com"


def test_marshal():
    namespace_obj = SimpleNamespace(
        name="John",
        age=30,
        address=SimpleNamespace(city="New York", zipcode="10001"),
        contacts=[
            SimpleNamespace(type="phone", number="123-4567"),
            SimpleNamespace(type="email", address="john@example.com"),
        ],
    )
    json_data = marshal(namespace_obj)

    assert isinstance(json_data, dict)
    assert json_data["name"] == "John"
    assert json_data["age"] == 30
    assert isinstance(json_data["address"], dict)
    assert json_data["address"]["city"] == "New York"
    assert json_data["address"]["zipcode"] == "10001"
    assert isinstance(json_data["contacts"], list)
    assert isinstance(json_data["contacts"][0], dict)
    assert json_data["contacts"][0]["type"] == "phone"
    assert json_data["contacts"][0]["number"] == "123-4567"
    assert json_data["contacts"][1]["type"] == "email"
    assert json_data["contacts"][1]["address"] == "john@example.com"


def test_unmarshal_and_marshal():
    json_data = {
        "name": "John",
        "age": 30,
        "address": {"city": "New York", "zipcode": "10001"},
        "contacts": [
            {"type": "phone", "number": "123-4567"},
            {"type": "email", "address": "john@example.com"},
        ],
    }
    namespace_obj = unmarshal(json_data)
    marshalled_json_data = marshal(namespace_obj)

    assert json_data == marshalled_json_data
