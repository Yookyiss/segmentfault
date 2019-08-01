import datetime

from django.contrib.auth import get_user_model
from config.settings.local import EMAIL_HOST_USER
from config import celery_app

User = get_user_model()
from django.core.mail import send_mail


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


@celery_app.task()
def periodic_notification():
    """定期提醒长时间未登陆的用户"""

    today = datetime.datetime.now()
    last_login_time = datetime.timedelta(days=7)
    day = today-last_login_time
    users = User.objects.filter(last_login__lt=day)
    recipient_list = [user.email for user in users]
    if recipient_list:
        send_mail('segmentfault','最近有好多人又发布了新的问题，快来回答吧～！',EMAIL_HOST_USER,recipient_list)
    return 'email alredy post'


@celery_app.task()
def message_remind():

    """当有新消息到来并且用户在3天内没有登陆，发送邮件通知"""
    today = datetime.datetime.now()
    last_login_time = datetime.timedelta(days=3)
    day = today - last_login_time
    users = User.objects.filter(last_login__gt=day)
    recipient_list = [user.email for user in users]
    if recipient_list:
        send_mail('segmentfault', '你有一条新消息哦～', EMAIL_HOST_USER, recipient_list)
    return 'email alredy post'
