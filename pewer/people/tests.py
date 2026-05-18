from datetime import date

from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse
from .models import Person
from .services import fetch_and_save_people


def make_person(**kwargs):
    defaults = dict(
        gender='woman',
        first_name='Нонна',
        last_name='Шепелева',
        phone='+7 (972) 535-17-61',
        email='nonna@ya.ru',
        address='г. Ангарск, Ленина ул., д. 10',
        passport_num='4960 696872',
        passport_code='840-593',
        passport_otd='ОУФМС России по г. Ангарск',
        passport_date=date(2021, 8, 4),
        inn_fiz='429835765592',
        snils='70884090315',
        oms='4594234397084410',
    )
    defaults.update(kwargs)
    return Person.objects.create(**defaults)


API_ITEM = {
    'GenderCode': 'woman',
    'FirstName': 'Нонна',
    'LastName': 'Шепелева',
    'Phone': '+7 (972) 535-17-61',
    'Email': 'nonna@ya.ru',
    'Address': 'г. Ангарск, Ленина ул., д. 10',
    'PasportNum': '4960 696872',
    'PasportCode': '840-593',
    'PasportOtd': 'ОУФМС России по г. Ангарск',
    'PasportDate': '04.08.2021',
    'inn_fiz': '429835765592',
    'snils': '70884090315',
    'oms': '4594234397084410',
}


class FetchAndSavePeopleTest(TestCase):
    def setUp(self):
        Person.objects.all().delete()

    @patch('people.services.requests.get')
    def test_saves_list_response(self, mock_get):
        mock_get.return_value.json.return_value = [API_ITEM, API_ITEM]
        mock_get.return_value.raise_for_status = MagicMock()

        count = fetch_and_save_people(2)

        self.assertEqual(count, 2)
        self.assertEqual(Person.objects.count(), 2)

    @patch('people.services.requests.get')
    def test_saves_single_dict_response(self, mock_get):
        mock_get.return_value.json.return_value = API_ITEM
        mock_get.return_value.raise_for_status = MagicMock()

        count = fetch_and_save_people(1)

        self.assertEqual(count, 1)
        self.assertEqual(Person.objects.count(), 1)

    @patch('people.services.requests.get')
    def test_correct_fields_saved(self, mock_get):
        mock_get.return_value.json.return_value = [API_ITEM]
        mock_get.return_value.raise_for_status = MagicMock()

        fetch_and_save_people(1)

        person = Person.objects.get(email='nonna@ya.ru')
        self.assertEqual(person.gender, 'woman')
        self.assertEqual(person.first_name, 'Нонна')
        self.assertEqual(person.last_name, 'Шепелева')
        self.assertEqual(person.passport_num, '4960 696872')
        self.assertEqual(person.passport_date, date(2021, 8, 4))
        self.assertEqual(person.inn_fiz, '429835765592')

    @patch('people.services.requests.get')
    def test_http_error_raises(self, mock_get):
        mock_get.return_value.raise_for_status.side_effect = Exception('HTTP error')

        with self.assertRaises(Exception):
            fetch_and_save_people(1)


class IndexViewTest(TestCase):
    def setUp(self):
        Person.objects.all().delete()
        self.client = Client()
        for i in range(5):
            make_person(first_name=f'Имя{i}', email=f'user{i}@ya.ru')

    def test_get_returns_200(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_context_has_page_obj(self):
        response = self.client.get(reverse('index'))
        self.assertIn('page_obj', response.context)

    def test_pagination(self):
        Person.objects.all().delete()
        for i in range(25):
            make_person(first_name=f'Имя{i}', email=f'p{i}@ya.ru')

        response = self.client.get(reverse('index') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].number, 2)

    @patch('people.views.fetch_and_save_people')
    def test_post_calls_service(self, mock_fetch):
        self.client.post(reverse('index'), {'count': '10'})
        mock_fetch.assert_called_once_with(10)

    def test_post_empty_count_does_not_call_service(self):
        response = self.client.post(reverse('index'), {'count': ''})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Person.objects.count(), 5)


class PersonDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.person = make_person()

    def test_returns_200_for_existing(self):
        response = self.client.get(reverse('person_detail', args=[self.person.id]))
        self.assertEqual(response.status_code, 200)

    def test_returns_404_for_missing(self):
        response = self.client.get(reverse('person_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)

    def test_context_has_person(self):
        response = self.client.get(reverse('person_detail', args=[self.person.id]))
        self.assertEqual(response.context['person'], self.person)


class RandomPersonViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_returns_200(self):
        make_person()
        response = self.client.get(reverse('random'))
        self.assertEqual(response.status_code, 200)

    def test_returns_different_people(self):
        for i in range(20):
            make_person(first_name=f'Имя{i}', email=f'r{i}@ya.ru')

        ids = set()
        for _ in range(10):
            response = self.client.get(reverse('random'))
            ids.add(response.context['person'].id)

        self.assertGreater(len(ids), 1)
