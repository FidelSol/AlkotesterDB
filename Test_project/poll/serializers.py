from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tests, Photo


class TestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tests
        fields = ('tests_id', 'personal_id', 'expected_time', 'result_time', 'result')

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photo_id', 'personal_id', 'data_pub', 'data_photo')

class UserSerializer(serializers.ModelSerializer):
    tests = serializers.PrimaryKeyRelatedField(many=True, queryset=Tests.objects.all())
    photos = serializers.PrimaryKeyRelatedField(many=True, queryset=Photo.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'tests', 'photos']
        owner = serializers.ReadOnlyField(source='owner.username')