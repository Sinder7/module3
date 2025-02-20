from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from django.db.models import Q

from .serializers import MissionsSerializer, UserRegistrationSerializer
from .models import Missions, User


class GagarinView(APIView):
    def get(self, request):
        data = [
            {
                "mission": {
                    "name": "Восток 1",
                    "launch_details": {
                        "launch_date": "1961-04-12",
                        "launch_site": {
                            "name": "Космодром Байконур",
                            "location": {
                                "latitude": "45.9650000",
                                "longitude": "63.3050000"
                            }
                        }
                    },
                    "flight_duration": {
                        "hours": 1,
                        "minutes": 48
                    },
                    "spacecraft": {
                        "name": "Восток 3KA",
                        "manufacturer": "OKB-1",
                        "crew_capacity": 1
                    }
                },
                "landing": {
                    "date": "1961-04-12",
                    "site": {
                        "name": "Смеловка",
                        "country": "СССР",
                        "coordinates": {
                            "latitude": "51.2700000",
                            "longitude": "45.9970000"
                        }
                    },
                    "details": {
                        "parachute_landing": True,
                        "impact_velocity_mps": 7
                    }
                },
                "cosmonaut": {
                    "name": "Юрий Гагарин",
                    "birthdate": "1934-03-09",
                    "rank": "Старший лейтенант",
                    "bio": {
                        "early_life": "Родился в Клушино, Россия.",
                        "career": "Отобран в отряд космонавтов в 1960 году...",
                        "post_flight": "Стал международным героем."
                    }
                }
            }
        ]

        return Response({"data": data}, status=status.HTTP_200_OK)


class FlightView(APIView):
    def get(self, request):
        data = {
            "name": "Аполлон-11",
            "crew_capacity": 3,
            "cosmonaut": [
                {"name": "Нил Армстронг", "role": "Командир"},
                {"name": "Базз Олдрин", "role": "Пилот лунного модуля"},
                {"name": "Майкл Коллинз", "role": "Пилот командного модуля"}],
            "launch_details": {"launch_date": "1969-07-16",
                               "launch_site": {"name": "Космический центр имени Кеннеди", "latitude": "28.5721000",
                                               "longitude": "-80.6480000"}},
            "landing_details": {"landing_date": "1969-07-20",
                                "landing_site": {"name": "Море спокойствия", "latitude": "0.6740000",
                                                 "longitude": "23.4720000"}}}
        return Response({"data": data}, status=status.HTTP_200_OK)


class MissionView(APIView):
    def get(self, request):
        missions = Missions.objects.all()
        serializer = MissionsSerializer(missions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = MissionsSerializer(data=request.data.get("mission"))
        if serializer.is_valid():
            mission = serializer.save()
            return Response({"data": {"code": 201, "message": "Миссия добавлена"}})
        return Response(
            {
                "error": {
                    "code": 422,
                    "message": "Validation error",
                    "errors": serializer.errors,
                }
            }
        )


class MissionDetailes(APIView):
    def get_mission(self, mission_id):
        try:
            return Missions.objects.get(id=mission_id)
        except Missions.DoesNotExist:
            raise NotFound(detail={"message": "Not found", "code": 404})

    def delete(self, reqquest, mission_id):
        mission = self.get_mission(mission_id)
        mission.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    def patch(self, request, mission_id):
        mission = self.get_mission(mission_id)
        mission_data = request.data.get("mission")

        serializer = MissionsSerializer(mission, data=mission_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"data": {"code": 200, "message": "Миссия обновлена"}},
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "error": {
                    "code": 422,
                    "message": "Ошибка валидации",
                    "errors": serializer.errors
                }
            },
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


SPACE = [{"flight_number": "СФ-103", "destination": "Марс", "launch_date": "2025-05-15", "seats_available": 2},
         {"flight_number": "СФ-105", "destination": "Юпитер", "launch_date": "2024-06-01", "seats_available": 3}]


class SpadeView(APIView):
    def get(self, request):
        return Response(
            {
                "data": SPACE
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        space_data = request.data

        required_fields = {"flight_number", "destination", "launch_date", "seats_available"}
        if not required_fields.issubset(space_data.keys()):
            return Response({"error": {"code": 422, "message": "Ошибка валидации", "errors": "Все поля обязательны"}},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY, )

        SPACE.append(space_data)

        return Response({"data": {"code": 201, "message": "Космический полет создан"}}, status=status.HTTP_201_CREATED)


class SearchMissionsView(APIView):
    def get(self, request):
        query = request.GET.get("query", "").strip()

        if not query:
            return Response(
                {"error": {"code": 400, "message": "Параметр 'query' обязателен"}},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Поиск миссий по названию или имени пилота
        missions = Missions.objects.filter(
            Q(name__icontains=query) |
            Q(spacecraft__crew__name__icontains=query)
        ).distinct()

        # Формирование ответа
        results = [
            {
                "type": "Миссия",
                "name": mission.name,
                "launch_date": mission.launch_details.get("launch_date", ""),
                "landing_date": mission.landing_details.get("landing_date", ""),
                "crew": mission.spacecraft.get("crew", []),
                "landing_site": mission.landing_details.get("landing_site", {}).get("name", ""),
            }
            for mission in missions
        ]

        return Response({"data": results}, status=status.HTTP_200_OK)


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            # Создание нового пользователя
            user_data = serializer.validated_data
            user = User.objects.create_user(
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                patronymic=user_data['patronymic'],
                password=user_data['password'],
                birth_date=user_data['birth_date']
            )
            return Response(
                {
                    "data": {
                        "user": {
                            "name": f"{user.last_name} {user.first_name} {user.patronymic}",
                            "email": user.email
                        },
                        "code": 201,
                        "message": "Пользователь создан"
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "error": {
                    "code": 422,
                    "message": "Ошибка валидации",
                    "errors": serializer.errors
                }
            },
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
