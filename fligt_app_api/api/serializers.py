from rest_framework import serializers
from datetime import datetime

from .models import LunarMission


class LunarMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LunarMission
        fields = ['name', 'launch_details', 'landing_details', 'spacecraft']

    def validate_name(self, value):
        if not value.istitle():
            raise serializers.ValidationError("Название миссии должно начинаться с заглавной буквы")
        return value

    def validate_launch_details(self, value):
        if 'launch_date' in value:
            try:
                datetime.strptime(value['launch_date'], '%Y-%m-%d')
            except ValueError:
                raise serializers.ValidationError("Дата запуска должна быть в формате YYYY-MM-DD")
        return value

    def validate_landing_details(self, value):
        if 'landing_date' in value:
            try:
                datetime.strptime(value['landing_date'], '%Y-%m-%d')
            except ValueError:
                raise serializers.ValidationError("Дата посадки должна быть в формате YYYY-MM-DD")
        return value

    def validate_coordinates(self, value):
        if "latitude" in value or "longitude" in value:
            if not isinstance(value.get("latitude"), (float, int)) or not isinstance(value.get("longitude"),
                                                                                     (float, int)):
                raise serializers.ValidationError("Координаты должны быть числами с плавающей точкой.")
        return value


class WatermarkTextSerializer(serializers.Serializer):
    fileimage = serializers.ImageField(
        required=True,
        allow_empty_file=False,
    )
    message = serializers.CharField(
        required=True,
        min_length=10,
        max_length=20
    )
