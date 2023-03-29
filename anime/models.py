from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from django.utils import timezone
import datetime

# Create your models here.
class AnimeData(models.Model):
    anime_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=10)
    status = models.CharField(max_length=20)
    picture = models.URLField()
    sources = ArrayField(models.URLField())
    episodes = models.IntegerField()
    synonyms = ArrayField(models.CharField(max_length=255))
    tags = ArrayField(models.CharField(max_length=255))
    relations = ArrayField(models.URLField(), default=list)
    thumbnail = models.URLField()
    season_year = models.IntegerField(null=True, blank=True)
    season = models.CharField(max_length=10)

    def __str__(self):
        return self.title

class AnimeList(models.Model):
    STATUS_CHOICES = (
        ('watching', 'Watching'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
        ('plan to watch', 'Plan to Watch')
    )

    anime_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='plan to watch'
    )

    def __str__(self):
        return f"{self.user.username} - {self.anime_id} - {self.status}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anime_id = models.IntegerField()
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    def time_since_posted(self):
        now = timezone.now()
        time_difference = now - self.timestamp
        if time_difference < datetime.timedelta(minutes=1):
            return 'Just now'
        elif time_difference < datetime.timedelta(hours=1):
            minutes = int(time_difference.total_seconds() / 60)
            return f'{minutes} minutes ago'
        elif time_difference < datetime.timedelta(days=1):
            hours = int(time_difference.total_seconds() / 3600)
            return f'{hours} hours ago'
        elif time_difference < datetime.timedelta(weeks=1):
            days = int(time_difference.total_seconds() / 86400)
            return f'{days} days ago'
        elif time_difference < datetime.timedelta(weeks=4):
            weeks = int(time_difference.total_seconds() / 604800)
            return f'{weeks} weeks ago'
        elif time_difference < datetime.timedelta(days=365):
            months = int(time_difference.total_seconds() / 2592000)
            return f'{months} months ago'
        else:
            years = int(time_difference.total_seconds() / 31536000)
            return f'{years} years ago'

    def __str__(self):
        return f'{self.user.username}: {self.text}'