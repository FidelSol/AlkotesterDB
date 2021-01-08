from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

from .views import Table_tests, Table_persons, Card

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:personal_id>/', views.detail, name='detail'),
    path('poll/fail', views.test_fail, name='fail'),
    path('add_personal/', views.add_personal, name='add_p'),
    path('add_tests/', views.add_tests, name='add_t'),
    path('tests', Table_tests.as_view(), name='tests'),
    path('personals', Table_persons.as_view(), name='personals'),
    path('card/<int:personal_id>/', Card.as_view(), name='card'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
