# Generated by Django 4.2.6 on 2023-11-18 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0005_remove_voteanswer_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='votemodel',
            name='rerunable',
            field=models.BooleanField(default=False),
        ),
    ]