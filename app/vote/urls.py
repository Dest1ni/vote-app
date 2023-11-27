from django.urls import path
from .views import *

app_name = 'vote'

urlpatterns = [
    path('add_vote/', CreateVote.as_view(), name = 'vote-create'),
    path('profile/', UserVotes.as_view(), name = 'vote-profile'),
    path('my_vote/<int:pk>/', UserVote.as_view(), name = 'vote-detail'),
    path('add_choice_to_vote/<int:pk>/', AddOptionToVote.as_view(), name = 'vote-choice'),
    path('delete_vote/<int:pk>/', DeleteVote.as_view(), name = 'vote-delete'),
    path('publish_vote/<int:pk>/', PublishVote.as_view(), name = 'vote-publish'),
    path('vote/<int:pk>/',DetailVote.as_view(),name = "vote-published"),
    path('completed_votes/',CompletedVoteList.as_view(),name = "vote-completed"),
    path('add_user/<int:pk>',AddUsertoVote.as_view(),name = "vote-user"),
]