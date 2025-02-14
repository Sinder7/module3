from rest_framework.urls import path

from .views import GagarinView, FlightInfoView, LunarMissions, LunarMissionDetailView

urlpatterns = [
    path("gagarin-flight", GagarinView.as_view()),
    path('flight', FlightInfoView.as_view(), name='flight-info'),
    path('lunar-missions', LunarMissions.as_view(), name='flight-info'),
    path('lunar-missions/<int:mission_id>/', LunarMissionDetailView.as_view(), name='mission-detail'),

]
