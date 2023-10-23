from django.db import models

class BaseVoteFieldModel(models.Model):
    question = models.TextField()
    vote = models.BooleanField() 

class SurveyFormModel(models.Model):
    text_answer = models.TextField()
    # who create
    # creates for (Optional)

class VotingFormModel(models.Model):
    pass
    # who create
    # creates for (Optional)
    
class VoteFieldModel(BaseVoteFieldModel):
    vote_form = models.ForeignKey(VotingFormModel,on_delete=models.PROTECT)

class SurveyFieldModel(BaseVoteFieldModel):
    vote_form = models.ForeignKey(SurveyFormModel,on_delete=models.PROTECT)