
from django.urls import path
from .views import get_weather,Home_view,Contact_view

urlpatterns = [
    path('', Home_view.as_view(), name='home'),
    path('/get-weather',get_weather,name="get_weather"),
    path('/contact_view',Contact_view.as_view(),name="contact")
]
