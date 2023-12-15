from city import City

def test_city_info(cities, limit):
    try:
        city_instance = City(cities, limit)
        city_instance.city_get()
        print(f"Data for city {cities} with limit {limit} has been fetched.")
    except ValueError as e:
        print(e)

test_city_info(cities = ["Austin", "New York"], limit = 3)
