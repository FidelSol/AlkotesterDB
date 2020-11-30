from rest_framework import serializers

from .models import Tests


class TestsSerializer(serializers.Serializer):
    personal_id = serializers.IntegerField()
    expected_time = serializers.DateTimeField()
    result_time = serializers.DateTimeField()
    result = serializers.BooleanField()

    def create(self, validated_data):
        return Tests.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.personal_id = validated_data.get('personal_id', instance.personal_id)
        instance.expected_time = validated_data.get('expected_time', instance.expected_time)
        instance.result_time = validated_data.get('result_time', instance.result_time)
        instance.result = validated_data.get('result', instance.result)

        instance.save()
        return instance