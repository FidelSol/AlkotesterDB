from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import PersonalCreateView




urlpatterns = [
    path('', views.index, name='index'),
    path('<int:personal_id>/', views.detail, name='detail'),
    path('poll/fail', views.test_fail, name='fail'),
    path('add/', PersonalCreateView.as_view(), name='add'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
