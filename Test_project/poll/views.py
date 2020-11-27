
from django.shortcuts import render
from .models import Personal, Photo, Tests
from .forms import TestsForm, PhotoForm



def index(request):
    personals = Personal.objects.all()
    context = {'personals': personals}
    return render(request, 'poll/index.html', context)


def detail(request, personal_id):
    persona = Personal.objects.get(pk = personal_id)
    photos = Photo.objects.filter(personal__personal_id=personal_id)
    tests = Tests.objects.filter(personal__personal_id=personal_id)
    context = {'persona': persona, 'photos': photos, 'tests': tests}
    return render(request, 'poll/detail.html', context)

def test_fail(request):
   tests = Tests.objects.filter(result = False)
   personals = Personal.objects.filter(tests__result = False)
   context = {'tests': tests, 'personals': personals}
   return render(request, 'poll/fail.html', context)


def recieve_form(request):
    value_1 = request.POST.get('full_name')
    value_2 = request.POST.get('ext_id')
    value_3 = request.POST.get('expected_time')
    value_4 = request.POST.get('result_time')
    value_5 = request.POST.get('result')
    value_6 = request.POST.get('data_photo')
    personals = Personal.objects.all()
    test = Tests.objects.all()
    photos = Photo.objects.all()
    form_1 = TestsForm(request.POST, request.FILES)
    form_2 = PhotoForm(request.POST, request.FILES)


    if value_5 == 'on':
        value_5 = True
    else:
        value_5 = False

    if request.method == 'POST':
        form_1 = TestsForm(request.POST, request.FILES)
        form_2 = PhotoForm(request.POST, request.FILES)
        personals = Personal.objects.create(full_name=value_1, ext_id=value_2)
        test = personals.tests_set.create(personal=personals, result=value_5, expected_time=value_3, result_time=value_4)
        photos = personals.photo_set.create(personal=personals, data_photo=value_6)
        if form_1.is_valid() and form_2.is_valid():
            form_1.save()
            form_2.save()
            return render(request, 'poll/set.html')
        else:
            return render(request, 'poll/set.html', {'form_1': form_1, 'form_2': form_2})
    else:
        pass
    context = {'value_1': value_1, 'value_2': value_2, 'value_3': value_3, 'value_4': value_4, 'value_5': value_5, 'value_6': value_6, 'personals': personals, 'test': test, 'form_1': form_1, 'form_2': form_2, 'photos': photos}
    return render(request, 'poll/set.html', context)

def add_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'poll/tests.html')
    else:
        form = PhotoForm()
    return render(request, 'poll/tests.html', {
        'form': form
    })









