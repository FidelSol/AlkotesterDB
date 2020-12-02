from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import TestsView, SingleTestsView, PhotoView, SinglePhotoView, UserView, SingleUserView, UserProfileListCreateView, userProfileDetailView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.auth import views as auth_views



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
    path('', auth_views.LoginView.as_view(template_name="poll/registration/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name="poll/registration/logout.html"), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="poll/registration/password_reset_form.html"), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="poll/registration/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="poll/registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="poll/registration/password_reset_complete.html"), name='password_reset_complete'),
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name="poll/registration/password_change_form.html"), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name="poll/registration/password_change_done.html"), name='password_change_done'),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('poll', views.index, name='index'),
    path('<int:personal_id>/', views.detail, name='detail'),
    path('poll/fail', views.test_fail, name='fail'),
    path('set/', views.recieve_form, name='set'),
    path('tests/', TestsView.as_view(),),
    path('tests/<int:pk>/', SingleTestsView.as_view(),),
    path('photo/', PhotoView.as_view(),),
    path('photo/<int:pk>/', SinglePhotoView.as_view(),),
    path('users/', UserView.as_view()),
    path('users/<int:pk>/', SingleUserView.as_view()),
    path("all-profiles", UserProfileListCreateView.as_view(), name="all-profiles"),
    path("profile/<int:pk>",userProfileDetailView.as_view(),name="profile"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
