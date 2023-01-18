from django.urls import path
from .views import*


urlpatterns = [
    path('reg/',SignUp.as_view(),name="reg"),
    path('log/',LoginView.as_view(),name="log"),
    path('logout/',SignOut.as_view(),name="logout"),
]
