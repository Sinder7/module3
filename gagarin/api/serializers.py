import re
from datetime import datetime

from rest_framework import serializers

from .models import Missions, User


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


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'patronymic', 'email', 'password', 'birth_date']

    def validate_first_name(self, value):
        if not value.istitle():
            raise serializers.ValidationError("Имя должно начинаться с заглавной буквы")
        return value

    def validate_last_name(self, value):
        if not value.istitle():
            raise serializers.ValidationError("Фамилия должна начинаться с заглавной буквы")
        return value

    def validate_patronymic(self, value):
        if not value.istitle():
            raise serializers.ValidationError("Отчество должно начинаться с заглавной буквы")
        return value

    def validate_password(self, value):
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну строчную букву")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("Пароль должен содержать хотя бы одну цифру")
        return value

