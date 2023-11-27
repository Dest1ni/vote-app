from typing import Any
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpResponseBadRequest,HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *

class CreateSurvey(LoginRequiredMixin,CreateView):
    model = SurveyModel
    template_name = 'survey/create_survey.html'
    fields = ['name','rerunable','for_everyone']
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        survey = form.save(commit= False)
        survey.who_create = self.request.user
        survey.save()
        return super().form_valid(form)

class AddOptionToSurvey(LoginRequiredMixin,CreateView): # Как то нужно прописать action в форме а там нужно передать pk вопрос в том как его получить ничего не изменяя тут
    model = SurveyQuestionModel
    template_name = 'survey/create_template/create_question.html'
    fields = ['question']

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        question = form.save(commit=False)
        survey = SurveyModel.objects.filter(pk = self.kwargs['pk']).first()
        if survey == None:
            return HttpResponseBadRequest('Такого опроса не существует')
        if survey.who_create != self.request.user:
            return HttpResponseBadRequest('Вы не можете изменить не пренадлежащий вам опрос')
        question.survey = survey
        question.save()
        return super().form_valid(form)

    def get_queryset(self):
        queryset = super().get_queryset()
        print(queryset)
        return queryset

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        print(context)
        return context
    
    def get_success_url(self) -> str:
        pk = self.kwargs['pk']
        return reverse_lazy('survey:survey-detail', kwargs= {'pk':pk})
    
class DetailSurvey(LoginRequiredMixin,DetailView):
    model = SurveyModel
    template_name = 'survey/detail_template/detail_survey.html'
    context_object_name = 'survey'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        survey = self.get_object()
        questions = SurveyQuestionModel.objects.filter(survey = survey).all()
        context['questions'] = questions
        print(context['questions'])
        #for question in context['questions']:
        print(context)
        return context


