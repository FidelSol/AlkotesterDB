from rest_framework import serializers

from .models import Tests


class TestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tests
        fields = ('tests_id', 'personal_id', 'expected_time', 'result_time', 'result')

