# Generated by Django 2.2.2 on 2019-06-22 11:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CircleMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.UUID('43ad1409-15bb-4202-a44a-3361507dc37d'), editable=False, unique=True)),
                ('context', models.TextField(verbose_name='内容')),
                ('is_comment', models.BooleanField(default=False, verbose_name='是否是评论')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('edit_time', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('like', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='点赞用户')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='message_parent', to='circle.CircleMessage', verbose_name='自关联')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='message_user', to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '动态与评论表',
                'verbose_name_plural': '动态与评论表',
                'ordering': ['-create_time'],
            },
        ),
    ]
