import re
from datetime import datetime


from rest_framework import serializers

from .models import User, Mission


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "patronymic", "birth_date", "password"]


    def validate_first_name(self,value):
        if not value.istitle():
            raise serializers.ValidationError("Имя должно начинаться с заглавной буквы")
        return value

    def validate_last_name(self,value):
        if not value.istitle():
            raise serializers.ValidationError("Фамилия должно начинаться с заглавной буквы")
        return value

    def validate_patronymic(self,value):
        if not value.istitle():
            raise serializers.ValidationError("Отчество должно начинаться с заглавной буквы")
        return value

    def validate_password(self, value):
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError("Пароль должен содержать строчную букву")
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Пароль должен содержать заглавную букву")
        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError("Пароль должен содержать цифру")
        return value


class MissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ["name", "launch_details", "landing_details", "spacecraft"]

    def validate_name(self, value):
        if not value.istitle():
            raise serializers.ValidationError("Имя должно начинаться с заглавной буквы")
        return value

    def validate(self, value):
        launch_details = value.get("launch_details", {})
        landing_details = value.get("landing_details", {})

        launch_date = launch_details.get("launch_date")
        if launch_date:
            try:
                datetime.strptime(launch_date, "%Y-%m-%d")
            except ValueError:
                raise serializers.ValidationError("Неверный формат даты launch_date")

        landing_date = landing_details.get("landing_date")
        if landing_date:
            try:
                datetime.strptime(landing_date, "%Y-%m-%d")
            except ValueError:
                raise serializers.ValidationError("Неверный формат даты landing_date")

        return value