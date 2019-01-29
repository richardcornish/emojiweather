from django.urls import path

from .views import AskCommandView, ChuckCommandView, PrintCommandView, FactCommandView, HotCommandView, WeatherCommandView


urlpatterns = [
    path('ask', AskCommandView.as_view()),
    path('fact', FactCommandView.as_view()),
    path('chuck', ChuckCommandView.as_view()),
    path('print', PrintCommandView.as_view()),
    path('hot', HotCommandView.as_view()),
    path('weather', WeatherCommandView.as_view()),
]
