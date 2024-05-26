import json
import hashlib
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class HashableModel(models.Model):
    def hash_field(self, field_name):
        if getattr(self, field_name):
            return hashlib.sha256(getattr(self, field_name).encode()).hexdigest()
        return None

    def unhash_field(self, field_name, hashed_value):
        try:
            return hashlib.sha256(hashed_value.encode()).hexdigest() == getattr(self, field_name)
        except AttributeError:
            return False


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


class UserInfo(HashableModel):
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

    hashed_username = models.CharField(max_length=64, blank=True)
    hashed_user_id = models.CharField(max_length=64, blank=True)
    hashed_is_account_closed = models.CharField(max_length=64, blank=True)
    hashed_first_name = models.CharField(max_length=64, blank=True)
    hashed_last_name = models.CharField(max_length=64, blank=True)
    hashed_bdate = models.CharField(max_length=64, blank=True)
    hashed_status_text = models.CharField(max_length=64, blank=True)
    hashed_country = models.CharField(max_length=64, blank=True)
    hashed_city = models.CharField(max_length=64, blank=True)
    hashed_home_town = models.CharField(max_length=64, blank=True)
    hashed_schools = models.CharField(max_length=64, blank=True)
    hashed_university = models.CharField(max_length=64, blank=True)
    hashed_faculty = models.CharField(max_length=64, blank=True)
    hashed_graduation = models.CharField(max_length=64, blank=True)
    hashed_education_form = models.CharField(max_length=64, blank=True)
    hashed_education_status = models.CharField(max_length=64, blank=True)
    hashed_langs = models.CharField(max_length=64, blank=True)
    hashed_friends = models.CharField(max_length=64, blank=True)
    hashed_followers_count = models.CharField(max_length=64, blank=True)
    hashed_crop_photo = models.CharField(max_length=64, blank=True)
    hashed_albums = models.CharField(max_length=64, blank=True)
    hashed_audios = models.CharField(max_length=64, blank=True)
    hashed_gifts = models.CharField(max_length=64, blank=True)
    hashed_groups = models.CharField(max_length=64, blank=True)
    hashed_photos = models.CharField(max_length=64, blank=True)
    hashed_subscriptions_on_profiles = models.CharField(max_length=64, blank=True)
    hashed_videos = models.CharField(max_length=64, blank=True)
    hashed_length_posts = models.CharField(max_length=64, blank=True)
    hashed_activities = models.CharField(max_length=64, blank=True)
    hashed_interests = models.CharField(max_length=64, blank=True)
    hashed_religion = models.CharField(max_length=64, blank=True)
    hashed_books = models.CharField(max_length=64, blank=True)
    hashed_games = models.CharField(max_length=64, blank=True)
    hashed_movies = models.CharField(max_length=64, blank=True)
    hashed_music = models.CharField(max_length=64, blank=True)
    hashed_quotes = models.CharField(max_length=64, blank=True)
    hashed_inspired_by = models.CharField(max_length=64, blank=True)
    hashed_verified = models.CharField(max_length=64, blank=True)
    hashed_frends_data = models.CharField(max_length=64, blank=True)


    def save(self, *args, **kwargs):
        self.hashed_username = self.hash_field('username')
        self.hashed_user_id = self.hash_field('user_id')
        self.hashed_is_account_closed = self.hash_field('is_account_closed')
        self.hashed_first_name = self.hash_field('first_name')
        self.hashed_last_name = self.hash_field('last_name')
        self.hashed_bdate = self.hash_field('bdate')
        self.hashed_status_text = self.hash_field('status_text')
        self.hashed_country = self.hash_field('country')
        self.hashed_city = self.hash_field('city')
        self.hashed_home_town = self.hash_field('home_town')
        self.hashed_schools = self.hash_field('schools')
        self.hashed_university = self.hash_field('university')
        self.hashed_faculty = self.hash_field('faculty')
        self.hashed_graduation = self.hash_field('graduation')
        self.hashed_education_form = self.hash_field('education_form')
        self.hashed_education_status = self.hash_field('education_status')
        self.hashed_langs = self.hash_field('langs')
        self.hashed_friends = self.hash_field('friends')
        self.hashed_followers_count = self.hash_field('followers_count')
        self.hashed_crop_photo = self.hash_field('crop_photo')
        self.hashed_albums = self.hash_field('albums')
        self.hashed_audios = self.hash_field('audios')
        self.hashed_gifts = self.hash_field('gifts')
        self.hashed_groups = self.hash_field('groups')
        self.hashed_photos = self.hash_field('photos')
        self.hashed_subscriptions_on_profiles = self.hash_field('subscriptions_on_profiles')
        self.hashed_videos = self.hash_field('videos')
        self.hashed_length_posts = self.hash_field('length_posts')
        self.hashed_activities = self.hash_field('activities')
        self.hashed_interests = self.hash_field('interests')
        self.hashed_religion = self.hash_field('religion')
        self.hashed_books = self.hash_field('books')
        self.hashed_games = self.hash_field('games')
        self.hashed_movies = self.hash_field('movies')
        self.hashed_music = self.hash_field('music')
        self.hashed_quotes = self.hash_field('quotes')
        self.hashed_inspired_by = self.hash_field('inspired_by')
        self.hashed_verified = self.hash_field('verified')
        self.hashed_frends_data = self.hash_field('frends_data')

        super().save(*args, **kwargs)
    # потом
    # def verify_field1(self, value):
    #     return self.unhash_field('original_field1', value)
    #
    # def verify_field2(self, value):
    #     return self.unhash_field('original_field2', value)



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
