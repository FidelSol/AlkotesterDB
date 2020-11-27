from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:personal_id>/', views.detail, name='detail'),
    path('poll/fail', views.test_fail, name='fail'),
    path('set/', views.recieve_form, name='set'),
    path('poll/tests', views.add_photo, name='tests'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
