from event_id import ID
from pytest import fixture

@fixture
def reverse_keys():
    return ["country", "state", "city", "classification",
            "recalling_firm", "product_type", "event_id"]

def test_reverse_info(reverse_keys):
    """Tests an API call to get a reverse info based on event_id"""
    reverse_instance = ID(["85253", "62750"])
    response = reverse_instance.id_get()

    assert isinstance(response,dict)
    assert response["results"][0]["event_id"] == "85253", "The ID should be in the response"
    assert set(reverse_keys).issubset(response["results"][0].keys()), "All keys should be in the response"

test_reverse_info(["country", "state", "city", "classification",
            "recalling_firm", "product_type", "event_id"])