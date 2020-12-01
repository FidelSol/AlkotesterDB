from django.conf.urls import url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import TestsView, SingleTestsView, PhotoView, SinglePhotoView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', views.index, name='index'),
    path('<int:personal_id>/', views.detail, name='detail'),
    path('poll/fail', views.test_fail, name='fail'),
    path('set/', views.recieve_form, name='set'),
    path('tests/', TestsView.as_view(),),
    path('tests/<int:pk>/', SingleTestsView.as_view(),),
    path('photo/', PhotoView.as_view(),),
    path('photo/<int:pk>/', SinglePhotoView.as_view(),),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
