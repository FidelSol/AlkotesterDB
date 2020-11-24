
from django.shortcuts import render
from .models import Personal, Photo, Tests
from django.views.generic.edit import CreateView
from .forms import PersonalForm

def index(request):
    personals = Personal.objects.all()
    context = {'personals': personals}
    return render(request, 'poll/index.html', context)


def detail(request, personal_id):
    persona = Personal.objects.get(pk=personal_id)
    photos = Photo.objects.filter(personal__personal_id=personal_id)
    tests = Tests.objects.filter(personal__personal_id=personal_id)
    context = {'persona': persona, 'photos': photos, 'tests': tests}
    return render(request, 'poll/detail.html', context)

def test_fail(request):
   tests = Tests.objects.filter(result = False)
   personals = Personal.objects.filter(tests__result = False)
   context = {'tests': tests, 'personals': personals}
   return render(request, 'poll/fail.html', context)


class PersonalCreateView(CreateView):
    template_name = 'poll/create.html'
    form_class = PersonalForm
    success_url = '/poll/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def recieve_form(request):
    value_1 = request.POST.get('full_name')
    value_2 = request.POST.get('ext_id')
    value_3 = request.POST.get('expected_time')
    value_4 = request.POST.get('result_time')
    value_5 = request.POST.get('result')
    personal = Personal.objects.all()
    tests = Tests.objects.all()

    if value_5 == 'on':
        value_5 = True
    else:
        value_5 = False

    if request.method == 'POST':
        personal = Personal.objects.create(full_name=value_1, ext_id=value_2)
        tests.personal = Tests.objects.create(personal=personal, expected_time=value_3, result_time=value_4, result=value_5)
        personal = Personal.objects.get(full_name=value_1, ext_id=value_2)
        tests = Tests.objects.get(personal=personal, expected_time=value_3, result_time=value_4, result=value_5)
        tests.personal = personal
        tests.save()
    else:
        pass
    context = {'value_1': value_1, 'value_2': value_2, 'value_3': value_3, 'value_4': value_4, 'value_5': value_5, 'personal': personal, 'tests': tests}
    return render(request, 'poll/set.html', context)


