from django.urls import path
from .views import *

app_name = 'survey'

urlpatterns = [
    path('create/', CreateSurvey.as_view(), name = 'survey-create'),
    path('detail/<int:pk>/', DetailSurvey.as_view(), name = 'survey-detail'),
    path('add_question/<int:pk>/',AddOptionToSurvey.as_view(), name = 'survey-question'),
]