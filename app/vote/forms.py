from django import forms
from .models import *


class CreateVoteForm(forms.ModelForm):
    class Meta:
        model = VoteModel
        fields = ['name','question'] 

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