# Generated by Django 4.2.6 on 2023-11-20 15:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0007_surveymodel_surveyuser_surveyquestionmodel_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveymodel',
            name='who_create',
        ),
        migrations.AlterUniqueTogether(
            name='surveyquestionmodel',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='surveyquestionmodel',
            name='survey',
        ),
        migrations.RemoveField(
            model_name='surveyuser',
            name='survey',
        ),
        migrations.RemoveField(
            model_name='surveyuser',
            name='user',
        ),
        migrations.DeleteModel(
            name='SurveyAnswerOption',
        ),
        migrations.DeleteModel(
            name='SurveyModel',
        ),
        migrations.DeleteModel(
            name='SurveyQuestionModel',
        ),
        migrations.DeleteModel(
            name='SurveyUser',
        ),
    ]
