
from django.shortcuts import render
from .models import Personal, Photo, Tests
from django.forms import inlineformset_factory
from django.views.generic.edit import CreateView
from .forms import PersonalForm
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect




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


class PersonalCreateView(CreateView):
    template_name = 'poll/create.html'
    form_class = PersonalForm
    success_url = '/poll/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AddTestsView(CreateView):
    template_name = 'poll/set_forms.html'
    success_url = '/poll/'

    if request.method == 'POST':
        form = TestsForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/poll/')
    else:
        form = PersonalForm()

    return render(request, 'name.html', {'form': form})









