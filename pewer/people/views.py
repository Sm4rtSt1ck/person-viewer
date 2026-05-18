import random

from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Person
from .services import fetch_and_save_people


def index(request):
    if request.method == 'POST':
        count = int(request.POST.get('count') or 0)
        if count > 0:
            fetch_and_save_people(count)
        return redirect('index')

    people = Person.objects.all().order_by('id')
    paginator = Paginator(people, 20)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    return render(request, 'people/index.html', {'page_obj': page_obj})


def person_detail(request, user_id):
    person = get_object_or_404(Person, id=user_id)
    return render(request, 'people/person_detail.html', {'person': person})


def random_person(request):
    ids = Person.objects.values_list('id', flat=True)
    random_id = random.choice(list(ids))
    person = Person.objects.get(id=random_id)
    return render(request, 'people/person_detail.html', {'person': person})
