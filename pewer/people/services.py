import requests
from .models import Person


API_URL = "https://api.randomdatatools.ru/"


def fetch_and_save_people(count: int) -> int:
    response = requests.get(API_URL, params={"count": count})
    response.raise_for_status()
    data = response.json()

    people = [
        Person(
            gender=item["GenderCode"],
            first_name=item["FirstName"],
            last_name=item["LastName"],
            phone=item["Phone"],
            email=item["Email"],
            address=item["Address"],
        )
        for item in data
    ]

    Person.objects.bulk_create(people)
    return len(people)
