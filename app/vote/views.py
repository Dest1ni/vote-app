from typing import Any
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models.query import QuerySet
from django.forms.forms import BaseForm
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView,DetailView,ListView,DeleteView,FormView,View,UpdateView
from .forms import *
from .models import *


class CreateVote(LoginRequiredMixin,CreateView):

    login_url = reverse_lazy('users:users-login')
    template_name = 'vote/create_template/create_vote.html'

    form_class = CreateVoteForm
    
    model = VoteModel

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        vote = form.save(commit=False)
        vote.who_create = self.request.user
        vote.save()
        if not vote.for_everyone:
            vote_user = VoteUser(vote = vote,user = self.request.user)
            vote_user.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("vote:vote-detail",kwargs = {'pk':self.object.pk})


class AddOptionToVote(LoginRequiredMixin,CreateView):

    login_url = reverse_lazy('users:users-login')
    template_name = 'vote/create_template/create_option.html'
    model = VoteOption
    form_class = AddAnswerChoiceToVoteForm
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        try:
            option = form.save(commit=False)
            vote = VoteModel.objects.filter(pk = self.kwargs['pk']).first()
            if vote.published == True:
                return HttpResponseBadRequest("Нельзя добавить вариант ответа для опубликованного голосования")
            option.vote_model = vote  # Сюда не просто пк а модель саму пихнуть надо 
            option.save()
            return super().form_valid(form)
        except IntegrityError:
            return HttpResponse("Варинат ответа должен быть уникален в рамках одного голосования",status = 500)


    def get_success_url(self) -> str:
        return reverse_lazy('vote:vote-detail',kwargs = {'pk':self.kwargs['pk']})


class UserVotes(LoginRequiredMixin,ListView):
    model = VoteModel
    context_object_name = "votes"
    template_name = "users/profile/user_votes.html"
    login_url = reverse_lazy('users:users-login')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['votes'] = context['votes'].filter(who_create = self.request.user.pk).all()
        return context

class UserVote(LoginRequiredMixin,DetailView):
    model = VoteModel
    context_object_name = "vote"
    template_name = "users/profile/user_vote.html"
    login_url = reverse_lazy('users:users-login')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['options'] = VoteOption.objects.filter(vote_model = self.get_object().pk)
        return context
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        vote = self.get_object()
        if vote.who_create != self.request.user:
            return HttpResponseBadRequest("У вас нет доступа к этому голосованию")
        return super().get(request, *args, **kwargs)


class DeleteVote(LoginRequiredMixin,DeleteView):
    model = VoteModel
    success_url = reverse_lazy("vote:vote-profile")
    template_name = "vote/delete_template/delete_vote.html"
    login_url = reverse_lazy('users:users-login')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        vote = self.get_object()
        if vote.who_create != self.request.user:
            return HttpResponseBadRequest("У вас нет доступа к этому голосованию")
        return super().get(request, *args, **kwargs)

class SearchVote(LoginRequiredMixin,FormView): # Реализовать как в ап6
    form_class = SeacrchVoteForm
    login_url = reverse_lazy('users:users-login')

    def form_valid(self, form: Any) -> HttpResponse:
        pk = form.cleaned_data['pk']
        if VoteModel.objects.get(pk = pk).published == False:
            return HttpResponseBadRequest("У вас нет доступа к этому голосованию")
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy("vote:vote")

class ListVote(LoginRequiredMixin,ListView):
    model = VoteModel
    template_name = "vote/list_vote.html"
    context_object_name = "votes"
    paginate_by = 5

    #def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #    context = super().get_context_data(**kwargs)
    #    votes = self.get_queryset()
    #    context['votes'] = votes.order_by('name')
    #    return context
    
    def get_queryset(self) -> QuerySet[Any]:
        return VoteModel.objects.order_by('name')
    
class PublishVote(LoginRequiredMixin,View):
    login_url = reverse_lazy('users:users-login')
    def post(self, request, *args, **kwargs): # Щас бы jquery знать :(
        pk = self.kwargs['pk']
        vote = VoteModel.objects.get(pk = pk)
        if len(VoteOption.objects.filter(vote_model = vote).all()) <= 1:
            return HttpResponseBadRequest("Нельзя выставить голосование с одним или без вариантов ответа")
        if self.request.user.pk != vote.who_create.pk:
            return HttpResponseBadRequest("У вас нет доступа к этому голосованию")
        else:
            vote.published = True
            vote.save()
        return HttpResponseRedirect(reverse_lazy("vote:vote-detail", kwargs = {'pk':pk}))
    
class DetailVote(LoginRequiredMixin,FormView):
    template_name = "vote/detail_template/detail_vote.html"
    form_class = VoteAnswerForm
    login_url = reverse_lazy('users:users-login')

    def get_form_kwargs(self) -> dict[str, Any]:
        kwargs =  super().get_form_kwargs()
        kwargs['choice'] = [(option.pk, option.choice) for option in VoteOption.objects.filter(vote_model=self.kwargs['pk'])]
        return kwargs
    
    def form_valid(self, form: Any) -> HttpResponse:
        data = form.cleaned_data
        if len(data) != 1:
            return HttpResponseBadRequest("Нужно выбрать только один вариант ответа")
        
        answer = VoteOption.objects.filter(pk = int(data['choice'])).first()
        user = self.request.user
        vote_model = self.get_context_data()['vote']
        if not vote_model.for_everyone:
            if not VoteUser.objects.filter(user = user,vote = vote_model).all():
                return HttpResponseBadRequest("У вас нет доступа к этому голосованию")
        if (not VoteAnswer.objects.filter(option__vote_model = vote_model, user = user).exists()) and (vote_model.rerunable == False):
            answer = VoteAnswer(user = user,
                                option = answer,
                                )
            answer.save()
        elif vote_model.rerunable == True:
            answer = VoteAnswer(user = user,
                                option = answer,
                                )
            answer.save()
        else:
            return HttpResponseBadRequest("На это голосование запрещено отвечать повторно")
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('vote:vote-detail',kwargs = {'pk':self.kwargs['pk']})
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context =  super().get_context_data(**kwargs)
        context['vote'] = VoteModel.objects.filter(pk = self.kwargs['pk']).first()
        return context

class CompletedVoteList(LoginRequiredMixin,ListView):
    model = VoteAnswer
    login_url = reverse_lazy('users:users-login')
    template_name = "users/profile/completed_vote.html"
    context_object_name = "votes"
    paginate_by = 3

    def get_queryset(self) -> QuerySet[Any]:
        return VoteAnswer.objects.filter(user = self.request.user).all()

class AddUsertoVote(LoginRequiredMixin,FormView):
    form_class = AddUserToVoteForm
    template_name = "vote/create_template/add_user_to_vote.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
    
    def form_valid(self, form: Any) -> HttpResponse:
        user_pk = form.cleaned_data['pk']
        vote_model = VoteModel.objects.filter(pk = self.kwargs['pk']).first()
        user = UserModel.objects.filter(pk = user_pk).first()
        if self.request.user == vote_model.who_create:
            user_vote = VoteUser(user = user,vote = vote_model)
            user_vote.save()
        else:
            return HttpResponseBadRequest("У вас нет доступа к этому голосованию")
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('vote:vote-detail', kwargs = {'pk':self.kwargs['pk']})

class UpdateVote(LoginRequiredMixin,UpdateView):
    model = VoteModel
    form_class = UpdateVoteForm
    template_name = "vote/update_vote.html"
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        vote = self.get_object()
        if vote.who_create != self.request.user:
            return HttpResponseBadRequest("У вас нет доступа к этому голосованию")
        if vote.published:
            return HttpResponseBadRequest("Нельзя обновить опубликованное голосование")
        data = form.cleaned_data
        if data['name'].strip() == '':
            return HttpResponseBadRequest("Название не может быть пустым")
        if data['question'].strip() == '':
            return HttpResponseBadRequest("Название не может быть пустым")
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy("vote:vote-detail",kwargs = {"pk":self.get_object().pk})
    

class UpdateVoteOption(LoginRequiredMixin,UpdateView):
    model = VoteOption
    fields = ['choice']
    template_name = "vote/update_template/update_option.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        vote = self.get_object().vote_model
        if vote.who_create != self.request.user:
            return HttpResponseBadRequest("У вас нет доступа к этому голосованию")
        if vote.published:
            return HttpResponseBadRequest("Нельзя обновить опубликованное голосование")
        data = form.cleaned_data
        if data['choice'].strip() == '':
            return HttpResponseBadRequest("Вариант не может быть пустым")
        
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        option = self.get_object()
        vote_model = option.vote_model
        return reverse_lazy("vote:vote-detail",kwargs = {"pk":vote_model.pk})