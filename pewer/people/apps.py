from django.apps import AppConfig


class PeopleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'people'

    def ready(self):
        from django.db.models.signals import post_migrate
        post_migrate.connect(load_initial_data, sender=self)


def load_initial_data(sender, **kwargs):
    from .models import Person
    from .services import fetch_and_save_people

    if Person.objects.exists():
        return

    fetch_and_save_people(1000)
