from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView,CreateView
from .forms import *
from .models import *


class CreateVote(LoginRequiredMixin,CreateView):

    # login_url = reverse
    template_name = 'vote/create_vote.html'
    # success_url = reverse
    
    form_class = CreateVoteForm()
    
    model = VoteModel

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        vote = form.save(commit=False)
        vote.who_create = self.request.user
        vote.save()
        return super().form_valid(form)

class CreateSurvey(LoginRequiredMixin,CreateView):

    # login_url = reverse
    # template_name =
    # success_url = reverse

    form_class = CreateSurveyForm

    def form_valid(self, form) -> HttpResponse:
        survey = form.save(commit=False)
        user = self.request.user
        survey.who_create = user
        survey.save()
        return super().form_valid(form)

class AddAnswerChoiceToVote(LoginRequiredMixin,CreateView):

    # login_url = reverse
    # template_name =
    # success_url = reverse

    form_class = AddAnswerChoiceToVoteForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        choice = form.save(commit=False)
        choice.vote_model = self.kwargs['pk']
        choice.save()
        return super().form_valid(form)

class AddQestionToSurvey(LoginRequiredMixin,CreateView):

    # login_url = reverse
    # template_name =
    # success_url = reverse

    form_class = AddQestionToSurveyForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        question = form.save(commit=False)
        question.survey = self.kwargs['pk']
        question.save()
        return super().form_valid(form)

class AddAnswerOptionToSurveyQuestion(LoginRequiredMixin,CreateView):
    # login_url = reverse
    # template_name =
    # success_url = reverse

    form_class = AddAnswerOptionToSurveyForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        choice = form.save(commit = False)
        choice.question_survey_model = self.kwargs['pk']
        choice.save()
        return super().form_valid(form)
