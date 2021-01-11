
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormMixin
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from .models import Personal, Photo, Tests
from .forms import TestsForm, PersonalForm, PhotoFormSet
from .serializers import TestsSerializer, PhotoSerializer, UserSerializer, PersonalSerializer
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.views.generic import View, DetailView
from django.contrib.auth import get_user_model
User = get_user_model()


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


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response

class Table_tests(AjaxableResponseMixin, View):
    template_name ='inter/tests_table.html'
    personals = Personal.objects.all()
    model = Tests

    def get(self, request):
        personals = self.personals
        return render(request, 'inter/tests_table.html', {'personals': personals})

    def post(self, request, *args, **kwargs):
        personals = self.personals
        return render(request, 'inter/tests_table.html', {'personals': personals})


class Table_persons(AjaxableResponseMixin, View):
    template_name = 'inter/personal_table.html'
    model = Personal
    personals = Personal.objects.all()
    fails = Personal.objects.filter(tests__result=False).distinct()
    f = len(fails)
    context = {'personals': personals, 'fails': fails, 'f': f}

    def get(self, request):
        context = self.context
        return render(request, 'inter/personal_table.html', context)

    def post(self, request, *args, **kwargs):
        context = self.context
        return render(request, 'inter/personal_table.html', context)

class Card(AjaxableResponseMixin, FormMixin, DetailView):
    template_name = 'inter/card.html'
    model = Personal
    pk_url_kwarg = "personal_id"
    form_class = PhotoFormSet

    def get_success_url(self):
        return reverse('card', kwargs={'pk': self.object.pk})


    def get_context_data(self, **kwargs):
        context = super(Card, self).get_context_data(**kwargs)
        pk = self.object.pk
        context['persona'] = Personal.objects.get(personal_id=pk)
        context['photos'] = Photo.objects.filter(personal__personal_id=pk)
        context['tests'] = Tests.objects.filter(personal__personal_id=pk)
        context['formset'] = PhotoFormSet(instance=context['persona'])
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        return render(request, 'inter/card.html', context)

class Card_photo(Card):
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        context['formset'] = PhotoFormSet(request.POST, request.FILES, instance=context['persona'])
        if context['formset'].is_valid():
            context['formset'].save()
        return HttpResponseRedirect(reverse('card', kwargs={'personal_id': self.object.pk}))
