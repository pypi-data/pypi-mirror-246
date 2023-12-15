from django.urls import include, path

from .views import run_demo

urlpatterns = [
    path("rt_messages/", include("pluto_rt.urls")),
    path('', run_demo),
]
