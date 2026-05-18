from datetime import datetime
import requests
from .models import Person


API_URL = "https://api.randomdatatools.ru/"


def fetch_and_save_people(count: int) -> int:
    response = requests.get(API_URL, params={"count": count})
    response.raise_for_status()
    data = response.json()

    if isinstance(data, dict):
            data = [data]

    people = [
        Person(
            gender=item["GenderCode"],
            first_name=item["FirstName"],
            last_name=item["LastName"],
            phone=item["Phone"],
            email=item["Email"],
            address=item["Address"],
            passport_num=item["PasportNum"],
            passport_code=item["PasportCode"],
            passport_otd=item["PasportOtd"],
            passport_date=datetime.strptime(item["PasportDate"], "%d.%m.%Y").date(),
            inn_fiz=item["inn_fiz"],
            snils=item["snils"],
            oms=item["oms"],
        )
        for item in data
    ]

    Person.objects.bulk_create(people)
    return len(people)
