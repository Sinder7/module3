from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_201_CREATED, HTTP_204_NO_CONTENT, \
    HTTP_404_NOT_FOUND

from .serializer import RegisterSerializer, MissionSerializer
from .models import Mission


class GagarinView(APIView):
    def get(self, request):
        data = [{"mission": {"name": "Восток 1", "launch_details": {"launch_date": "1961-04-12",
                                                                    "launch_site": {"name": "Космодром Байконур",
                                                                                    "location": {
                                                                                        "latitude": "45.9650000",
                                                                                        "longitude": "63.3050000"}}},
                             "flight_duration": {"hours": 1, "minutes": 48},
                             "spacecraft": {"name": "Восток 3KA", "manufacturer": "OKB-1", "crew_capacity": 1}},
                 "landing": {"date": "1961-04-12", "site": {"name": "Смеловка", "country": "СССР",
                                                            "coordinates": {"latitude": "51.2700000",
                                                                            "longitude": "45.9970000"}},
                             "details": {"parachute_landing": True, "impact_velocity_mps": 7}},
                 "cosmonaut": {"name": "Юрий Гагарин", "birthdate": "1934-03-09", "rank": "Старший лейтенант",
                               "bio": {"early_life": "Родился в Клушино, Россия.",
                                       "career": "Отобран в отряд космонавтов в 1960 году...",
                                       "post_flight": "Стал международным героем."}}}]
        return Response({"data": data}, status=HTTP_200_OK)


class FlightView(APIView):
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
        return Response(
            {
                "data": data
            },
            status=HTTP_200_OK
        )


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            user_data = serializer.validated_data
            return Response(
                {"data": {
                    "user": {
                        "name": f'{user_data["first_name"]} {user_data["last_name"]} {user_data["patronymic"]}'
                    },
                    "email": user_data["email"]},
                    "code": 201, "message": "Пользователь создан"
                },
                status=HTTP_201_CREATED
            )
        return Response(
            {
                "error": {
                    "code ": 422,
                    "message": "Validation error ",
                    "errors": serializer.errors
                }
            },
            status=HTTP_422_UNPROCESSABLE_ENTITY
        )


class MissionView(APIView):
    def get(self, request):
        mission = Mission.objects.all()
        serializer = MissionSerializer(mission, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request):
        serializer = MissionSerializer(data=request.data.get("mission"))
        if serializer.is_valid():
            mission = serializer.save()
            return Response({"data": {"code": 201, "message": "Миссия добавлена"}}, status=HTTP_201_CREATED)
        return Response(
            {
                "error": {
                    "code ": 422,
                    "message": "Validation error ",
                    "errors": serializer.errors
                }
            },
            status=HTTP_422_UNPROCESSABLE_ENTITY
        )


class MissionDetailes(APIView):
    def get_mission(self, id):
        try:
            return Mission.objects.get(id=id)
        except:
            raise NotFound(detail={"message": "Not found", "code": 404})

    def delete(self, request, mission_id):
        mission = self.get_mission(mission_id)
        mission.delete()
        return Response(status=HTTP_204_NO_CONTENT)

    def patch(self, request, mission_id):
        mission = self.get_mission(mission_id)
        mission_data = request.data.get("mission")

        serializer = MissionSerializer(mission, data=mission_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({"data": {"code": 200, "message": "Миссия обновлена"}}, status=HTTP_200_OK)

        return Response(
            {
                "error": {
                    "code ": 422,
                    "message": "Validation error ",
                    "errors": serializer.errors
                }
            },
            status=HTTP_422_UNPROCESSABLE_ENTITY
        )


SPACE = [{"flight_number": "СФ-103", "destination": "Марс", "launch_date": "2025-05-15", "seats_available": 2},
         {"flight_number": "СФ-105", "destination": "Юпитер", "launch_date": "2024-06-01", "seats_available": 3}]


class SpaceView(APIView):
    def get(self, request):
        return Response(
            {
                "data": SPACE
            },
            status=HTTP_200_OK
        )

    def post(self, request):
        space_data = request.data

        required_fields = {"flight_number", "destination", "launch_date", "seats_available"}
        if not required_fields.issubset(space_data.keys()):
            return Response({"error": {"code": 422, "message": "Ошибка валидации", "errors": "Все поля обязательны"}},
                            status=HTTP_422_UNPROCESSABLE_ENTITY, )

        SPACE.append(space_data)

        return Response(
            {"data": {"code": 201, "message": "Космический полет создан"}},
            status=HTTP_201_CREATED
        )


class BookSpace(APIView):
    def post(self, request):
        number = request.data.get("flight_number")

        if not number:
            return Response({"error": {"code": 422, "message": "Ошибка валидации", "errors": "Укажите номер рейса"}},
                            status=HTTP_422_UNPROCESSABLE_ENTITY, )

        for space in SPACE:
            if space["flight_number"] == number:
                if space["seats_available"] > 0:
                    return Response({"data": {"code": 201, "message": "Рейс забронирован"}}, status=HTTP_201_CREATED)
                else:
                    return Response({"data": {"code": 200, "message": "Свободных мест нет"}}, status=HTTP_200_OK)

        return Response({"message": "Not found", "code": 404}, status=HTTP_404_NOT_FOUND)
