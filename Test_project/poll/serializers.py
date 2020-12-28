from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Personal, Tests, Photo

class PersonalSerializer(serializers.ModelSerializer):
    personal_id = serializers.IntegerField(required=False)
    ext_id = serializers.IntegerField(required=False)
    full_name = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    position = serializers.CharField(required=False)
    punishment = serializers.IntegerField(required=False)

    class Meta:
        model = Personal
        fields = ('personal_id', 'ext_id', 'full_name', 'birth_date', 'position', 'punishment')

    def create(self, validated_data):
        return Personal.objects.create(**validated_data)

class TestsSerializer(serializers.ModelSerializer):
    tests_id = serializers.IntegerField(required=False)
    personal_id = serializers.IntegerField(required=False)
    expected_time = serializers.DateTimeField(required=False)
    result_time = serializers.DateTimeField(required=False)
    result = serializers.BooleanField(required=False)

    class Meta:
        model = Tests
        fields = ('tests_id', 'personal_id', 'expected_time', 'result_time', 'result')

    def create(self, validated_data):
        return Tests.objects.create(**validated_data)

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('photo_id', 'personal_id', 'data_pub', 'data_photo')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
        owner = serializers.ReadOnlyField(source='owner.username')

