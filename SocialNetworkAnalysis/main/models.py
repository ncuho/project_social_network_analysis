import json
from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Link(models.Model):
    link = models.CharField(max_length=100)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        to_field='id',
    )

    def __str__(self):
        return self.link

    class Meta:
        ordering = ("id",)


class UserInfo(models.Model):
    len_char_fild = 1000
    link = models.ForeignKey(
        Link,
        on_delete=models.CASCADE,
        to_field='id',
    )
    username = models.CharField(max_length=len_char_fild, null=True)
    user_id = models.CharField(max_length=len_char_fild, null=True)
    is_account_closed = models.CharField(max_length=len_char_fild, null=True)
    first_name = models.CharField(max_length=len_char_fild, null=True)
    last_name = models.CharField(max_length=len_char_fild, null=True)
    bdate = models.CharField(max_length=len_char_fild, null=True)
    status_text = models.CharField(max_length=len_char_fild, null=True)
    country = models.CharField(max_length=len_char_fild, null=True)
    city = models.CharField(max_length=len_char_fild, null=True)
    home_town = models.CharField(max_length=len_char_fild, null=True)
    schools = models.CharField(max_length=len_char_fild, null=True)
    university = models.CharField(max_length=len_char_fild, null=True)
    faculty = models.CharField(max_length=len_char_fild, null=True)
    graduation = models.CharField(max_length=len_char_fild, null=True)
    education_form = models.CharField(max_length=len_char_fild, null=True)
    education_status = models.CharField(max_length=len_char_fild, null=True)
    langs = models.CharField(max_length=len_char_fild, null=True)
    friends = models.CharField(max_length=len_char_fild, null=True)
    followers_count = models.CharField(max_length=len_char_fild, null=True)
    crop_photo = models.CharField(max_length=len_char_fild, null=True)
    albums = models.CharField(max_length=len_char_fild, null=True)
    audios = models.CharField(max_length=len_char_fild, null=True)
    gifts = models.CharField(max_length=len_char_fild, null=True)
    groups = models.CharField(max_length=len_char_fild, null=True)
    photos = models.CharField(max_length=len_char_fild, null=True)
    subscriptions_on_profiles = models.CharField(max_length=len_char_fild, null=True)
    videos = models.CharField(max_length=len_char_fild, null=True)
    length_posts = models.CharField(max_length=len_char_fild, null=True)
    activities = models.CharField(max_length=len_char_fild, null=True)
    interests = models.CharField(max_length=len_char_fild, null=True)
    religion = models.CharField(max_length=len_char_fild, null=True)
    books = models.CharField(max_length=len_char_fild, null=True)
    games = models.CharField(max_length=len_char_fild, null=True)
    movies = models.CharField(max_length=len_char_fild, null=True)
    music = models.CharField(max_length=len_char_fild, null=True)
    quotes = models.CharField(max_length=len_char_fild, null=True)
    inspired_by = models.CharField(max_length=len_char_fild, null=True)
    verified = models.CharField(max_length=len_char_fild, null=True)

    frends_data = models.CharField(max_length=len_char_fild**2, null=True)

    @property
    def get_info(self):
        return {"link": str(self.link),
                "username": str(self.username),
                "user_id": str(self.user_id),
                "is_account_closed": str(self.is_account_closed),
                "first_name": str(self.first_name),
                "last_name": str(self.last_name),
                "bdate": str(self.bdate),
                "status_text": str(self.status_text),
                "country": str(self.country),
                "city": str(self.city),
                "home_town": str(self.home_town),
                "schools": str(self.schools),
                "university": str(self.university),
                "faculty": str(self.faculty),
                "graduation": str(self.graduation),
                "education_form": str(self.education_form),
                "education_status": str(self.education_status),
                "langs": str(self.langs),
                "friends": str(self.friends),
                "followers_count": str(self.followers_count),
                "crop_photo": str(self.crop_photo),
                "albums": str(self.albums),
                "audios": str(self.audios),
                "gifts": str(self.gifts),
                "groups": str(self.groups),
                "photos": str(self.photos),
                "subscriptions_on_profiles": str(self.subscriptions_on_profiles),
                "videos": str(self.videos),
                "length_posts": str(self.length_posts),
                "activities": str(self.activities),
                "interests": str(self.interests),
                "religion": str(self.religion),
                "books": str(self.books),
                "games": str(self.games),
                "movies": str(self.movies),
                "music": str(self.music),
                "quotes": str(self.quotes),
                "inspired_by": str(self.inspired_by),
                "verified": str(self.verified),
                "frends_data": str(self.frends_data)}

    def __str__(self):
        return str({"link": self.link, "username": self.username, "user_id": self.user_id,
                    "is_account_closed": self.is_account_closed,
                    "first_name": self.first_name, "last_name": self.last_name, "bdate": self.bdate,
                    "status_text": self.status_text,
                    "country": self.country, "city": self.city, "home_town": self.home_town, "schools": self.schools,
                    "university": self.university, "faculty": self.faculty, "graduation": self.graduation,
                    "education_form": self.education_form,
                    "education_status": self.education_status, "langs": self.langs, "friends": self.friends,
                    "followers_count": self.followers_count, "crop_photo": self.crop_photo, "albums": self.albums,
                    "audios": self.audios, "gifts": self.gifts,
                    "groups": self.groups, "photos": self.photos,
                    "subscriptions_on_profiles": self.subscriptions_on_profiles,
                    "videos": self.videos, "length_posts": self.length_posts,
                    "activities": self.activities, "interests": self.interests, "religion": self.religion,
                    "books": self.books, "games": self.games,
                    "movies": self.movies, "music": self.music, "quotes": self.quotes, "inspired_by": self.inspired_by,
                    "verified": self.verified})

        class Meta:
            ordering = ("id",)
