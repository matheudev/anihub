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
    
class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    rank = models.IntegerField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    is_general_spoiler = models.BooleanField(default=False)
    is_media_spoiler = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Studio(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Staff(models.Model):
    id = models.IntegerField(primary_key=True)
    name_first = models.CharField(max_length=100, null=True, blank=True)
    name_last = models.CharField(max_length=100, null=True, blank=True)
    name_full = models.CharField(max_length=200, null=True, blank=True)
    name_native = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name_full or self.name_native or self.name_first

class Character(models.Model):
    id = models.IntegerField(primary_key=True)
    name_first = models.CharField(max_length=100, null=True, blank=True)
    name_last = models.CharField(max_length=100, null=True, blank=True)
    name_full = models.CharField(max_length=200, null=True, blank=True)
    name_native = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name_full or self.name_native or self.name_first

class ExternalLink(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.URLField(max_length=1000)
    site = models.CharField(max_length=500)

    def __str__(self):
        return self.site

class Ranking(models.Model):
    id = models.IntegerField(primary_key=True)
    rank = models.IntegerField()
    type = models.CharField(max_length=100)
    format = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    season = models.CharField(max_length=100, null=True, blank=True)
    all_time = models.BooleanField()
    context = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.rank} - {self.type} - {self.context}'

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Anime(models.Model):
    anilist_id = models.IntegerField(unique=True, primary_key=True)
    title_romaji = models.CharField(max_length=200)
    title_english = models.CharField(max_length=200, null=True, blank=True)
    title_native = models.CharField(max_length=200, null=True, blank=True)
    start_date_year = models.IntegerField(null=True, blank=True)
    start_date_month = models.IntegerField(null=True, blank=True)
    start_date_day = models.IntegerField(null=True, blank=True)
    end_date_year = models.IntegerField(null=True, blank=True)
    end_date_month = models.IntegerField(null=True, blank=True)
    end_date_day = models.IntegerField(null=True, blank=True)
    season = models.CharField(max_length=50, null=True, blank=True)
    season_year = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=200)
    format = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    episodes = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    chapters = models.IntegerField(null=True, blank=True)
    volumes = models.IntegerField(null=True, blank=True)
    is_adult = models.BooleanField(default=False)
    genres = models.ManyToManyField(Genre, related_name='anime_genres')
    average_score = models.IntegerField(null=True, blank=True)
    popularity = models.IntegerField(null=True, blank=True)
    source = models.CharField(max_length=100, default='UNKNOWN', null=True, blank=True)
    country_of_origin = models.CharField(max_length=2)
    cover_image_extra_large = models.URLField()
    cover_image_large = models.URLField()
    cover_image_medium = models.URLField()
    cover_image_color = models.CharField(max_length=50, null=True, blank=True)
    banner_image = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='anime_tags')
    studios = models.ManyToManyField(Studio, related_name='anime_studios')
    staff = models.ManyToManyField(Staff, related_name='anime_staff')
    characters = models.ManyToManyField(Character, related_name='anime_characters')
    external_links = models.ManyToManyField(ExternalLink, related_name='anime_external_links')
    trailer = models.URLField(null=True, blank=True)
    rankings = models.ManyToManyField(Ranking, related_name='anime_rankings')

    def __str__(self):
        return self.title_romaji