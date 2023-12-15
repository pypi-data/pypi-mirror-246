from date import Date

def test_date_info(start, end, limit):
    try:
        date_instance = Date(start, end, limit)
        date_instance.date_get()
    except ValueError as e:
        print(e)

test_date_info(start = 20150708, end = 20151225, limit = 5)