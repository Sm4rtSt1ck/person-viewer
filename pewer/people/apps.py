from django.apps import AppConfig


class PeopleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'people'

    def ready(self):
        from .models import Person
        from .services import fetch_and_save_people

        if Person.objects.exists():
            return

        fetch_and_save_people(1000)
