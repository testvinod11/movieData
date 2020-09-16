from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class BaseDateModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Movies(BaseDateModel):
    name = models.CharField(max_length=256, null=True, blank=True)
    released_year = models.PositiveIntegerField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    vote = models.PositiveBigIntegerField(null=True, blank=True)
    director_and_star = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.released_year})"


class UserWatchListMovie(BaseDateModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)


class UserWatchedMovie(UserWatchListMovie):
    pass
