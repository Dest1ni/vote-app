from typing import Any
from django.db import IntegrityError
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView,ListView
from .forms import *
from .models import *


class CreateVote(LoginRequiredMixin,CreateView):

    login_url = reverse_lazy('users:users-login')
    template_name = 'vote/create_template/create_vote.html'
    # success_url = reverse
    
    form_class = CreateVoteForm
    
    model = VoteModel

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        vote = form.save(commit=False)
        vote.who_create = self.request.user
        vote.save()
        return super().form_valid(form)

#class CreateSurvey(LoginRequiredMixin,CreateView):
#
#    login_url = reverse_lazy('users:users-login')
#    # template_name =
#    # success_url = reverse
#
#    form_class = CreateSurveyForm
#
#    def form_valid(self, form) -> HttpResponse:
#        survey = form.save(commit=False)
#        user = self.request.user
#        survey.who_create = user
#        survey.save()
#        return super().form_valid(form)

class AddOptionToVote(LoginRequiredMixin,CreateView):

    login_url = reverse_lazy('users:users-login')
    template_name = 'vote/create_template/create_option.html'
    model = VoteOption
    form_class = AddAnswerChoiceToVoteForm
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        try:
            option = form.save(commit=False)
            option.vote_model = VoteModel.objects.filter(pk = self.kwargs['pk']).first() # Сюда не просто пк а модель саму пихнуть надо 
            option.save()
            return super().form_valid(form)
        except IntegrityError:
            return HttpResponse("Варинат ответа должен быть уникален в рамках одного голосования",status = 500)


    def get_success_url(self) -> str:
        return reverse_lazy('vote:vote-detail',kwargs = {'pk':self.kwargs['pk']})

#class AddQestionToSurvey(LoginRequiredMixin,CreateView):
#
#    # login_url = reverse
#    # template_name =
#    # success_url = reverse
#
#    form_class = AddQestionToSurveyForm
#
#    def form_valid(self, form: BaseModelForm) -> HttpResponse:
#        question = form.save(commit=False)
#        question.survey = self.kwargs['pk']
#        question.save()
#        return super().form_valid(form)

#class AddAnswerOptionToSurveyQuestion(LoginRequiredMixin,CreateView):
#    # login_url = reverse
#    # template_name =
#    # success_url = reverse
#
#    form_class = AddAnswerOptionToSurveyForm
#
#    def form_valid(self, form: BaseModelForm) -> HttpResponse:
#        choice = form.save(commit = False)
#        choice.question_survey_model = self.kwargs['pk']
#        choice.save()
#        return super().form_valid(form)

class UserVotes(LoginRequiredMixin,ListView):
    model = VoteModel
    context_object_name = "votes"
    template_name = "users/profile/user_votes.html"
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['votes'] = context['votes'].filter(who_create = self.request.user.pk).all()
        return context

class UserVote(LoginRequiredMixin,DetailView):
    model = VoteModel
    context_object_name = "vote"
    template_name = "users/profile/user_vote.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['options'] = VoteOption.objects.filter(vote_model = self.get_object().pk)
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        vote = self.get_object()
        if vote.who_create != self.request.user:
            return HttpResponseBadRequest("У вас нет доступа к этому голосованию")
        return super().get(request, *args, **kwargs)