from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from .models import Personal, Photo, Tests
from .forms import TestsForm, PersonalForm, PhotoFormSet
from .serializers import TestsSerializer, PhotoSerializer, UserSerializer, PersonalSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from .utils import serialize_bootstraptable


@login_required
def index(request):
    personals = Personal.objects.all()
    context = {'personals': personals}
    return render(request, 'poll/index.html', context)

@login_required
def detail(request, personal_id):
    persona = Personal.objects.get(pk = personal_id)
    photos = Photo.objects.filter(personal__personal_id=personal_id)
    tests = Tests.objects.filter(personal__personal_id=personal_id)
    context = {'persona': persona, 'photos': photos, 'tests': tests}
    return render(request, 'poll/detail.html', context)

@login_required
def test_fail(request):
   tests = Tests.objects.filter(result=False)
   personals = Personal.objects.filter(tests__result = False).distinct()
   context = {'tests': tests, 'personals': personals}
   return render(request, 'poll/fail.html', context)

@login_required
def add_personal(request):
    form = PersonalForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("add_p"))
        else:
            form = PersonalForm(request.POST)
    return render(request, 'poll/add_personal.html', {"form": form})

@login_required
def add_tests(request):
    personals = Personal.objects.all()
    value_name = request.POST.get('full_name')
    form = TestsForm(request.POST)
    if request.method == "POST" and form.is_valid():
        a = form.save()
        persona = Personal.objects.get(full_name=value_name)
        test = Tests.objects.get(tests_id=a.tests_id)
        persona.tests_set.add(test)
        return HttpResponseRedirect(reverse("add_t"))
    else:
        form = TestsForm(request.POST)
    return render(request, 'poll/add_tests.html', {'personals': personals, 'form': form})

class PersonalsViewSet(viewsets.ModelViewSet):
    queryset = Personal.objects.prefetch_related('tests_set').all()
    serializer_class = PersonalSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]

class TestsViewSet(viewsets.ModelViewSet):
    queryset = Tests.objects.all()
    serializer_class = TestsSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]

class PhotosViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = [JSONParser, FormParser, MultiPartParser]

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def tests_for_json(request, *args, **kwargs):
    personals = Personal.objects.all()
    queryset = Tests.objects.all()
    json = serialize_bootstraptable(queryset)
    context = dict(json=json, personals=personals)
    return render(request, 'inter/tests_table.html', context)

def persons_for_json(request, *args, **kwargs):
    queryset = Personal.objects.all()
    fails = Personal.objects.filter(tests__result=False).distinct()
    f = len(fails)
    json = serialize_bootstraptable(queryset)
    context = dict(json=json, fails=fails, f=f)
    return render(request, 'inter/personal_table.html', context)

def card_for_json(request, personal_id):
    persona = Personal.objects.get(pk=personal_id)
    photos = Photo.objects.filter(personal__personal_id=personal_id)
    tests = Tests.objects.filter(personal__personal_id=personal_id)
    formset = PhotoFormSet(instance=persona)
    json_photos = serialize_bootstraptable(photos)
    json_tests = serialize_bootstraptable(tests)
    if request.method == 'POST':
        try:
            formset = PhotoFormSet(request.POST, request.FILES, instance=persona)
            if formset.is_valid():
                formset.save()
                return render(request, 'inter/card.html', {
                    'persona': persona, 'photos': photos, 'tests': tests, 'json_photos': json_photos,
                    'json_tests': json_tests, 'formset': formset
                })
        except ValidationError:
            formset = PhotoFormSet(instance=persona)
    context = {'persona': persona, 'photos': photos, 'tests': tests, 'json_photos': json_photos,
               'json_tests': json_tests, 'formset': formset}
    return render(request, 'inter/card.html', context)





