from FDA import food_reverse_info
from pytest import fixture

@fixture
def reverse_keys():
    return ["country", "state", "city", "classification",
            "recalling_firm", "product_type", "event_id"]

def test_reverse_info(reverse_keys):
    """Tests an API call to get a reverse info"""
    reverse_instance = food_reverse_info("85253")
    response = reverse_instance.info()

    assert isinstance(response,dict)
    assert response["results"][0]["event_id"] == "85253", "The ID should be in the response"
    assert set(reverse_keys).issubset(response["results"][0].keys()), "All keys should be in the response"

test_reverse_info(["country", "state", "city", "classification",
            "recalling_firm", "product_type", "event_id"])