
from django.shortcuts import render
from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from .license import IsOwnerProfileOrReadOnly
from .models import Personal, Photo, Tests, userProfile
from .forms import TestsForm, PhotoForm
from django.core.files.storage import FileSystemStorage
from .serializers import TestsSerializer, PhotoSerializer, UserSerializer, userProfileSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly


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

class TestsView(ListCreateAPIView):
    queryset = Tests.objects.all()
    serializer_class = TestsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        personal = get_object_or_404(Personal, id=self.request.data.get('personal_id'))
        return serializer.save(personal=personal)

class SingleTestsView(RetrieveUpdateDestroyAPIView):
    queryset = Tests.objects.all()
    serializer_class = TestsSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class PhotoView(ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    parser_classes = (FormParser, MultiPartParser)

    def perform_create(self, serializer):
        personal = get_object_or_404(Personal, id=self.request.data.get('personal_id'))
        return serializer.save(personal=personal)

class SinglePhotoView(RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class UserView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SingleUserView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



class UserProfileListCreateView(ListCreateAPIView):
    queryset=userProfile.objects.all()
    serializer_class=userProfileSerializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)

class userProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset=userProfile.objects.all()
    serializer_class=userProfileSerializer
    permission_classes=[IsOwnerProfileOrReadOnly, IsAuthenticated]
