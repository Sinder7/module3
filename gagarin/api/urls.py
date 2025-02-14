from django.urls import path

from .views import GagarinView, FlightView, MissionView, MissionDetailes

urlpatterns = [
    path("gagarin-flight", GagarinView.as_view()),
    path("flight", FlightView.as_view()),
    path("lunar-missions", MissionView.as_view()),
    path("lunar-missions/<int:mission_id>", MissionDetailes.as_view())
]
