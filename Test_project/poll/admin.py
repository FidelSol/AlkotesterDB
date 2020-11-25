from django.contrib import admin
from .models import Personal, Photo, Tests
# Register your models here.

class PersonalAdmin(admin.ModelAdmin):
    list_display = ('personal_id', 'ext_id', 'full_name')
    list_display_links = ('personal_id', 'ext_id', 'full_name')
    search_fields = ('personal_id', 'ext_id', 'full_name')

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('photo_id', 'personal', 'data_pub', 'data_photo')
    list_display_links = ('photo_id', 'personal', 'data_pub', 'data_photo')
    search_fields = ('photo_id', 'personal', 'data_pub', 'data_photo')

class TestsAdmin(admin.ModelAdmin):
    list_display = ('tests_id', 'personal', 'expected_time', 'result_time')
    list_display_links = ('tests_id', 'personal', 'expected_time', 'result_time')
    search_fields = ('tests_id', 'personal', 'expected_time', 'result_time')

admin.site.register(Personal, PersonalAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Tests, TestsAdmin)