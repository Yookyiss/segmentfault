# Generated by Django 2.2.2 on 2019-07-30 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_gain_votes'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='brithday',
            field=models.DateField(blank=True, null=True, verbose_name='生日'),
        ),
    ]
