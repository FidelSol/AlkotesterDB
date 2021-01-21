
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import Personal, Tests, Photo, CustomUser



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
    personal = serializers.PrimaryKeyRelatedField(many=True, queryset=Personal.objects.all())
    tests = serializers.PrimaryKeyRelatedField(many=True, queryset=Tests.objects.all())
    photo = serializers.PrimaryKeyRelatedField(many=True, queryset=Photo.objects.all())
    owner = serializers.ReadOnlyField(source='owner.username')
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role', 'personal', 'tests', 'photo', 'owner', 'token']


