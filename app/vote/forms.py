from collections.abc import Mapping
from typing import Any
from django import forms
from django.forms.fields import Field
from django.forms.utils import ErrorList
from .models import *


class CreateVoteForm(forms.ModelForm):
    class Meta:
        model = VoteModel
        fields = ['name','question','rerunable','for_everyone'] 

#class CreateSurveyForm(forms.ModelForm):
#    class Meta:
#        model = SurveyModel
#        fields = ['name'] 
#
class AddAnswerChoiceToVoteForm(forms.ModelForm):
    class Meta:
        model = VoteOption
        fields = ['choice'] 

#class AddQestionToSurveyForm(forms.ModelForm):
#    class Meta:
#        model = SurveyQuestionModel
#        fields = ['question']
#
#class AddAnswerOptionToSurveyForm(forms.ModelForm):
#    class Meta:
#        model = SurveyAnswerOption
#        fields = ['choice']

class SeacrchVoteForm(forms.Form):
    pk = forms.CharField(required=True)

class VoteAnswerForm(forms.Form):

    choice = forms.ChoiceField(widget=forms.RadioSelect,
                                choices=[])
    
    def __init__(self,*args,**kwargs) -> None:
        choices = kwargs.pop('choice')
        super(VoteAnswerForm, self).__init__(*args, **kwargs)
        self.fields['choice'].choices = choices

class AddUserToVoteForm(forms.Form):
    pk = forms.CharField(max_length=255)

class UpdateVoteForm(forms.ModelForm):
    name = forms.CharField(max_length=255,required = False)
    for_everyone = forms.BooleanField(required = False)
    rerunable = forms.BooleanField(required = False)
    question = forms.CharField(max_length=255,required = False)
    class Meta:
        model = VoteModel
        fields = ['name','for_everyone','rerunable','question']
    