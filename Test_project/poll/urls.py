
from django.urls import path


from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.index, name='index'),
    path('<int:personal_id>/', views.detail, name='detail'),
    path('poll/fail', views.test_fail, name='fail'),
    path('set/', views.recieve_form, name='set'),
    path('jsons/tests', views.tests_for_json, name='jsons_tests'),
    path('jsons/personals', views.persons_for_json, name='jsons_personals'),
    path('jsons/card/<int:personal_id>/', views.card_for_json, name='jsons_card'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
