from classification import Classification

def test_classification_info(class_type, limit):
    try:
        classification_instance = Classification(class_type, limit)
        classification_instance.class_info()
        print(f"Data for classification {class_type} with limit {limit} has been fetched.")
    except ValueError as e:
        print(e)

test_classification_info(3, 5)

