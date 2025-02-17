from django.urls import path

from .views import GagarinView, FlightView, MissionView, MissionDetailes, SpadeView, SearchMissionsView, \
    UserRegistrationView

urlpatterns = [
    path("gagarin-flight", GagarinView.as_view()),
    path("flight", FlightView.as_view()),
    path("lunar-missions", MissionView.as_view()),
    path("lunar-missions/<int:mission_id>", MissionDetailes.as_view()),
    path("space-flights", SpadeView.as_view()),
    path("search", SearchMissionsView.as_view()),
    path("registration/", UserRegistrationView.as_view())
]
