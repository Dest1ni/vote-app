# Generated by Django 4.2.6 on 2023-10-23 16:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseVoteFieldModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('vote', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='SurveyFormModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_answer', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='VotingFormModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='VoteFieldModel',
            fields=[
                ('basevotefieldmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vote.basevotefieldmodel')),
                ('vote_form', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vote.votingformmodel')),
            ],
            bases=('vote.basevotefieldmodel',),
        ),
        migrations.CreateModel(
            name='SurveyFieldModel',
            fields=[
                ('basevotefieldmodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='vote.basevotefieldmodel')),
                ('vote_form', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='vote.surveyformmodel')),
            ],
            bases=('vote.basevotefieldmodel',),
        ),
    ]