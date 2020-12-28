from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:personal_id>/', views.detail, name='detail'),
    path('poll/fail', views.test_fail, name='fail'),
    path('set/', views.recieve_form, name='set'),
    path('add_personal/', views.add_personal, name='add_p'),
    path('tests', views.tests_for_json, name='tests'),
    path('personals', views.persons_for_json, name='personals'),
    path('card/<int:personal_id>/', views.card_for_json, name='card'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
