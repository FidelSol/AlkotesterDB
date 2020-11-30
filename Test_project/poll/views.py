
from django.shortcuts import render
from rest_framework.generics import get_object_or_404

from .models import Personal, Photo, Tests
from .forms import TestsForm, PhotoForm
from django.core.files.storage import FileSystemStorage
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TestsSerializer


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

    personals = Personal.objects.all()
    test = Tests.objects.all()
    photos = Photo.objects.all()
    form_1 = TestsForm(request.POST)

    if value_5 == 'on':
        value_5 = True
    else:
        value_5 = False

    if request.method == 'POST' and request.FILES['data_photo']:
        form_1 = TestsForm(request.POST)
        personals = Personal.objects.create(full_name=value_1, ext_id=value_2)
        test = personals.tests_set.create(personal=personals, result=value_5, expected_time=value_3, result_time=value_4)

        data_photo = request.FILES['data_photo']
        fs = FileSystemStorage()
        filename = fs.save(data_photo.name, data_photo)
        uploaded_file_url = fs.url(filename)
        photos = personals.photo_set.create(personal=personals, data_photo=data_photo)
        return render(request, 'poll/set.html', {
            'uploaded_file_url': uploaded_file_url
        })

    else:
        pass
    context = {'value_1': value_1, 'value_2': value_2, 'value_3': value_3, 'value_4': value_4, 'value_5': value_5, 'personals': personals, 'test': test, 'form_1': form_1, 'photos': photos}
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

class TestsView(APIView):
    def get(self, request,  *args, **kwargs):
        tests = Tests.objects.all()
        serializer = TestsSerializer(tests, many=True)
        return Response({"tests": serializer.data})

    def post(self, request):
        tests = request.data.get('tests')
        serializer = TestsSerializer(data=tests)
        if serializer.is_valid(raise_exception=True):
            tests_saved = serializer.save()
        return Response({"success": "Test '{}' created successfully".format(tests_saved.personal_id)})

    def put(self, request, pk):
        saved_tests = get_object_or_404(Tests.objects.all(), pk=pk)
        data = request.data.get('tests')
        serializer = TestsSerializer(instance=saved_tests, data=data, partial=True)

        if serializer.is_valid(raise_exception=True):
            tests_saved = serializer.save()

        return Response({
            "success": "Test '{}' updated successfully".format(tests_saved.result)
        })

    def delete(self, request, pk):
        tests = get_object_or_404(Tests.objects.all(), pk=pk)
        tests.delete()
        return Response({
            "message": "Test with id `{}` has been deleted.".format(pk)
        }, status=204)




