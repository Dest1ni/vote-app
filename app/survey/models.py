from django.db import models
from users.models import UserModel


class SurveyModel(models.Model):
    """
    Модель опроса
    """
    name = models.CharField(null=False,max_length=255)
    who_create = models.ForeignKey(UserModel,models.CASCADE)
    published = models.BooleanField(default=False)
    for_everyone = models.BooleanField(default=True)
    rerunable = models.BooleanField(default=False)

class SurveyQuestionModel(models.Model):
    """
    Модель вопроса для опроса
    """
    question = models.CharField(null=False,max_length=255)
    survey = models.ForeignKey(SurveyModel,models.PROTECT)

    class Meta:
        unique_together = [['question','survey']]

class SurveyOption(models.Model):
    """
    Модель варианта овтета для вопроса опроса
    """
    question_survey_model = models.ForeignKey(SurveyQuestionModel,models.DO_NOTHING)
    option = models.CharField(null = False,max_length=255)

class SurveyAnswerOption(models.Model):
    """
    Модель ответа для вопроса опроса
    """
    choice = models.CharField(null=False,max_length=255)
    answer = models.BooleanField(null=True)
    free_answer = models.CharField(null=True,max_length=255)
    question_survey_model = models.ForeignKey(SurveyQuestionModel,models.PROTECT)

class SurveyUser(models.Model):
    """
    Модель m-t-m Пользователь <-> опрос
    """
    user = models.ForeignKey(UserModel,models.CASCADE)
    survey = models.ForeignKey(SurveyModel,models.CASCADE)
