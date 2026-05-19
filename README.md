# Person Viewer

> Person Viewer is a Django web application that fetches and stores random person data from an external API. On startup, the server automatically loads 1000 (in fact, it loads 100, due to API limitations) people into a SQLite database. The main page displays all stored people in a paginated table with gender, name, phone, email, and address, and allows loading additional people by specifying a count. Each person has a dedicated profile page accessible by their ID, displaying detailed information including passport data, INN, SNILS, and OMS number, and a random person endpoint returns a different person on every request. The project includes unit tests with mocked external API calls.


## Installation

1. Clone the repository:
```bash
git clone "https://github.com/Sm4rtSt1ck/person-viewer"
```

2. Activate the virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Apply migrations
```bash
cd pewer
python manage.py migrate
```

4. Run the server:
```bash
python manage.py runserver
```

5. Check out the result at: `127.0.0.1:8000`


## P.S.
Django выбран, потому что задача типична для CRUD-веб-приложения: внешний API, БД, отображение. В Django уже есть ORM, роутинг, шаблоны, тесты, для которых не нужны лишние зависимости.\
SQLite полностью покрывает требования к данному приложению и выбран для простоты локального запуска, так как нет внешних зависимостей, а при необходимости можно перейти на PostgreSQL изменением одной строки в settings.py.


## License

Code is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.
