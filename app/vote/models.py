from django.db import models
from users.models import UserModel
    

class VoteModel(models.Model):
    """
    Модель голосования
    """
    name = models.CharField(null=False)
    who_create = models.ForeignKey(UserModel,models.CASCADE)
    question = models.CharField(null=False)

class VoteAnswerOption(models.Model):
    """
    Модель ответа для голосования
    """
    choice = models.CharField(null=False)
    answer = models.BooleanField(null=True)
    vote_model = models.ForeignKey(VoteModel,models.PROTECT)

class SurveyModel(models.Model):
    """
    Модель опроса
    """
    name = models.CharField(null=False)
    who_create = models.ForeignKey(UserModel,models.CASCADE)

class SurveyQuestionModel(models.Model):
    """
    Модель вопроса для опроса
    """
    question = models.CharField(null=False)
    survey = models.ForeignKey(SurveyModel,models.PROTECT)
    free_answer = models.CharField(null=True)

class SurveyAnswerOption(models.Model):
    """
    Модель ответа для вопроса опроса
    """
    choice = models.CharField(null=False)
    answer = models.BooleanField(null=True)
    question_survey_model = models.ForeignKey(SurveyQuestionModel,models.PROTECT)

class VoteUser(models.Model):
    """
    Модель m-t-m Пользователь <-> Голосование
    """
    user = models.ForeignKey(UserModel,models.CASCADE)
    vote = models.ForeignKey(VoteModel,models.CASCADE)

class SurveyUser(models.Model):
    """
    Модель m-t-m Пользователь <-> опрос
    """
    user = models.ForeignKey(UserModel,models.CASCADE)
    survey = models.ForeignKey(SurveyModel,models.CASCADE)
