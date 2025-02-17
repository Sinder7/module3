from django.urls import path

from .views import GagarinView, RegisterView, FlightView, MissionView, MissionDetailes, SpaceView, BookSpace

urlpatterns = [
    path("gagarin-flight", GagarinView.as_view()),
    path("registration/", RegisterView.as_view()),
    path("flight", FlightView.as_view()),
    path("lunar-missions", MissionView.as_view()),
    path("lunar-missions/<int:mission_id>", MissionDetailes.as_view()),
    path("space-flights", SpaceView.as_view()),
    path("book-flight", BookSpace.as_view())
]
