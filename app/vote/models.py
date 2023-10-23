from django.db import models
from users.models import UserModel

class BaseVoteFieldModel(models.Model):
    """ 
    Базовое модель поля голосования/опроса 
    """
    question = models.TextField(null=False)
    vote = models.BooleanField() 

class SurveyFormModel(models.Model):
    """
    Модель опроса
    """
    text_answer = models.TextField()
    who_create = models.ForeignKey(UserModel,on_delete=models.CASCADE,null=False)

class VotingFormModel(models.Model):
    """
    Модель голосования
    """
    who_create = models.ForeignKey(UserModel,on_delete=models.CASCADE,null=False)

class VoteFieldModel(BaseVoteFieldModel):
    """
    Модель вопрос -> голосование
    """
    vote_form = models.ForeignKey(VotingFormModel,on_delete=models.PROTECT)

class SurveyFieldModel(BaseVoteFieldModel):
    """
    Модель вопрос -> опрос
    """
    vote_form = models.ForeignKey(SurveyFormModel,on_delete=models.PROTECT)

class SurveyUserRelationship(models.Model):
    """
    Модель юзер -> опрос
    """
    survey = models.ForeignKey(SurveyFormModel,on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)

class VoteUserRelationship(models.Model):
    """
    Модель юзер -> голосование
    """
    vote = models.ForeignKey(VotingFormModel,on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)