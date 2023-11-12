from django.db import models
from users.models import UserModel
    

class VoteModel(models.Model):
    """
    Модель голосования
    """
    name = models.CharField(null=False,max_length=255)
    who_create = models.ForeignKey(UserModel,models.CASCADE)
    question = models.CharField(null=False,max_length=255)
    published = models.BooleanField(default=False)
    for_everyone = models.BooleanField(default=True)

class VoteOption(models.Model):
    """
    Модель варианта для голосования
    """
    choice = models.CharField(null=False,max_length=255)
    vote_model = models.ForeignKey(VoteModel,models.PROTECT)
    
    class Meta:
        unique_together = [["choice","vote_model"]]
        
class VoteAnswer(models.Model):
    """
    Модель ответа для голосования
    """
    answer = models.BooleanField(null = False)
    option = models.ForeignKey(VoteOption,models.CASCADE)
    user = models.ForeignKey(UserModel,models.CASCADE)
    
class VoteUser(models.Model):
    """
    Модель m-t-m Пользователь <-> Голосование
    Показывает какой пользователь имеет доступ к голосованию
    """
    user = models.ForeignKey(UserModel,models.CASCADE)
    vote = models.ForeignKey(VoteModel,models.CASCADE)

#class SurveyModel(models.Model):
#    """
#    Модель опроса
#    """
#    name = models.CharField(null=False,max_length=255)
#    who_create = models.ForeignKey(UserModel,models.CASCADE)
#    published = models.BooleanField(default=False)
#    for_everyone = models.BooleanField(default=True)

#class SurveyQuestionModel(models.Model):
#    """
#    Модель вопроса для опроса
#    """
#    question = models.CharField(null=False,max_length=255)
#    survey = models.ForeignKey(SurveyModel,models.PROTECT)
#    free_answer = models.CharField(null=True,max_length=255)

#class SurveyAnswerOption(models.Model):
#    """
#    Модель ответа для вопроса опроса
#    """
#    choice = models.CharField(null=False,max_length=255)
#    answer = models.BooleanField(null=True)
#    question_survey_model = models.ForeignKey(SurveyQuestionModel,models.PROTECT)

#class SurveyUser(models.Model):
#    """
#    Модель m-t-m Пользователь <-> опрос
#    """
#    user = models.ForeignKey(UserModel,models.CASCADE)
#    survey = models.ForeignKey(SurveyModel,models.CASCADE)
