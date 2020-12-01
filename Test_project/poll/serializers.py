from rest_framework import serializers

from .models import Tests, Photo


class TestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tests
        fields = ('tests_id', 'personal_id', 'expected_time', 'result_time', 'result')

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photo_id', 'personal_id', 'data_pub', 'data_photo')