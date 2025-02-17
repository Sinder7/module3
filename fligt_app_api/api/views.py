from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound

from django.http import HttpResponse

from .serializers import LunarMissionSerializer, WatermarkTextSerializer
from .models import LunarMission


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


class FlightInfoView(APIView):
    def get(self, request):
        data = {
            "name": "Аполлон-11",
            "crew_capacity": 3,
            "cosmonaut": [
                {
                    "name": "Нил Армстронг",
                    "role": "Командир"
                },
                {
                    "name": "Базз Олдрин",
                    "role": "Пилот лунного модуля"
                },
                {
                    "name": "Майкл Коллинз",
                    "role": "Пилот командного модуля"
                }
            ],
            "launch_details": {
                "launch_date": "1969-07-16",
                "launch_site": {
                    "name": "Космический центр имени Кеннеди",
                    "latitude": "28.5721000",
                    "longitude": "-80.6480000"
                }
            },
            "landing_details": {
                "landing_date": "1969-07-20",
                "landing_site": {
                    "name": "Море спокойствия",
                    "latitude": "0.6740000",
                    "longitude": "23.4720000"
                }
            }
        }
        return Response({"data": data}, status=status.HTTP_200_OK)


class LunarMissions(APIView):
    def get(self, request):
        missions = LunarMission.objects.all()  # Получаем все миссии из базы данных
        serializer = LunarMissionSerializer(missions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LunarMissionSerializer(data=request.data.get("mission"))
        if serializer.is_valid():
            mission = serializer.save()  # Сохраняем миссию в базе данных
            return Response(
                {"data": {"code": 201, "message": "Миссия добавлена", }},
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "error": {
                    "code": 422,
                    "message": "Validated error",
                    "errors": serializer.errors
                }
            },
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


class LunarMissionDetailView(APIView):
    def get_object(self, mission_id):
        try:
            return LunarMission.objects.get(id=mission_id)
        except LunarMission.DoesNotExist:
            raise NotFound(detail="Миссия не найдена.")

    def patch(self, request, mission_id):
        mission = self.get_object(mission_id)
        mission_data = request.data.get('mission')

        serializer = LunarMissionSerializer(mission, data=mission_data, partial=True)

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

    def delete(self, request, mission_id):
        mission = self.get_object(mission_id)
        mission.delete()
        return Response(
            {"data": {"code": 200, "message": "Миссия удалена"}},
            status=status.HTTP_204_NO_CONTENT
        )