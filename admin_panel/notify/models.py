
import uuid

from django.db import models
from django.utils import timezone


class Destination(models.TextChoices):
    email = 'Email'
    sms = 'SMS'


class NotifierType(models.TextChoices):
    event = 'event', 'Some event'
    personal = 'personal', 'Unique letter'
    news = 'new', 'New movie/TV series'


class PriorityType(models.TextChoices):
    high = 'high', 'High'
    low = 'low', 'Low'


class DeliveryStatus(models.TextChoices):
    pending = 'pending'
    delivered = 'delivered'
    canceled = 'canceled'


class Status(models.TextChoices):
    done = 'done'
    undone = 'undone'


class Source(models.TextChoices):
    admin = 'Admin', 'Created by admin'
    auto = 'Auto', 'Generated automatically'
    service = 'Service', 'Generated by any service'


class Notice(models.Model):
    ntf_id = models.UUIDField(default=uuid.uuid4, editable=False)
    destination = models.CharField('Destination', max_length=255, choices=Destination.choices)
    type = models.CharField('Notification type', max_length=255, choices=NotifierType.choices)

    subject = models.CharField('Subject', max_length=255)
    title = models.CharField('Title', max_length=255, blank=True)
    text = models.TextField('Text', blank=True)
    content = models.CharField('Content (ex. movie_id)', max_length=255, blank=True)
    priority = models.CharField('Event priority', max_length=255,
                                choices=PriorityType.choices, default=PriorityType.high)
    time = models.DateTimeField('Sending time', default=timezone.now)
    source = models.CharField('Source', max_length=255, choices=Source.choices, default=Source.admin)

    status = models.CharField('Status', max_length=255, choices=Status.choices, default=Status.undone)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "notification\".\"notice"

        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'


# class Subscribe(models.TextChoices):
#     have_subscribe = 'True'
#     not_subscribe = 'False'
#
#
# class User(models.Model):
#     user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     email = models.CharField(max_length=255)
#     subscribe = models.CharField('Title', max_length=255)


# class NoticeUser(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE)
#     ntf_id = models.ForeignKey(Notice, on_delete=models.CASCADE)
#     status = models.CharField('Status', max_length=255, choices=DeliveryStatus.choices, default=DeliveryStatus.pending)
#     source = models.CharField('Source', max_length=255, choices=Source.choices, default=Source.admin)
#     type = models.CharField('Notification type', max_length=255)
