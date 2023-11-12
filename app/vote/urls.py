from django.urls import path
from .views import *

app_name = 'vote'

urlpatterns = [
    path('add_vote/', CreateVote.as_view(), name = 'vote-create'),
    path('my_votes/', UserVotes.as_view(), name = 'vote-list'),
    path('my_vote/<int:pk>/', UserVote.as_view(), name = 'vote-detail'),
    path('add_choice_to_vote/<int:pk>/', AddOptionToVote.as_view(), name = 'vote-choice'),
    # Надо как-то разделить логику показа голосвания до и после постинга
    #path('detail_vote/')
]