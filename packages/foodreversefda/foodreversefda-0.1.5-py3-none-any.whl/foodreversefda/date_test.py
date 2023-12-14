from date import Date

def test_date_info(start, end, limit):
    try:
        date_instance = Date(start, end, limit)
        date_instance.date_info()
    except ValueError as e:
        print(e)

test_date_info(20150708, 20180824,5)