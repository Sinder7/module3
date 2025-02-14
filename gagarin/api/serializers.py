from datetime import datetime

from rest_framework import serializers

from .models import Missions


class MissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Missions
        fields = ['name', 'launch_details', 'landing_details', 'spacecraft']

    def validate_name(self, value):
        """Проверка, что название миссии начинается с заглавной буквы"""
        if not value.istitle():
            raise serializers.ValidationError("Название миссии должно быть с заглавной буквы")
        return value

    def validate(self, data):
        """Глобальная валидация для проверки дат"""
        launch_details = data.get("launch_details", {})
        landing_details = data.get("landing_details", {})

        # Проверяем launch_date
        launch_date = launch_details.get("launch_date")
        if launch_date:
            try:
                datetime.strptime(launch_date, "%Y-%m-%d")
            except ValueError:
                raise serializers.ValidationError({"launch_details": "Неверный формат даты, используйте YYYY-MM-DD"})

        # Проверяем landing_date
        landing_date = landing_details.get("landing_date")
        if landing_date:
            try:
                datetime.strptime(landing_date, "%Y-%m-%d")
            except ValueError:
                raise serializers.ValidationError({"landing_details": "Неверный формат даты, используйте YYYY-MM-DD"})

        return data
