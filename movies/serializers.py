import django_filters
from rest_framework import serializers

from movies.models import *


# from django.contrib.auth.models import User


class MoviesFilterSet(django_filters.FilterSet):
   name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

   class Meta:
       model = Movies
       fields = ["name", ]


class MoviesCreateSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)


class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ("id", "name", "released_year", "rating", "vote", "director_and_star")


class UserWatchListMovieSerializer(serializers.ModelSerializer):
    movie = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_movie(obj):
        return MoviesSerializer(obj.movie).data

    class Meta:
        model = UserWatchListMovie
        fields = ("id", "movie")


class CreateUserWatchListSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(required=True, slug_field='id', queryset=Movies.objects.filter(is_active=True))

    def validate_movie(self, movie):
        user = self.context.get('user')
        if UserWatchListMovie.objects.filter(user=user, movie=movie, is_active=True).exists():
            raise serializers.ValidationError(f"Movie {movie.name} already in watch list")
        return movie

    def create(self, validated_data):
        movie = validated_data.get('movie')
        user = self.context.get('user')
        obj, created = UserWatchListMovie.objects.get_or_create(user=user, movie=movie)
        if not created:
            obj.is_active = True
            obj.save()
        return obj

    def to_representation(self, obj):
        attr = super().to_representation(obj)
        attr.__setitem__('movie', MoviesSerializer(obj.movie).data)
        return attr

    class Meta:
        model = UserWatchListMovie
        fields = ("id", "movie")


class UserWatchedMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWatchedMovie
        fields = ("id", "movie")

    def to_representation(self, obj):
        attr = super().to_representation(obj)
        attr.__setitem__('movie', MoviesSerializer(obj.movie).data)
        return attr


class CreateUserWatchedSerializer(serializers.ModelSerializer):
    movie = serializers.SlugRelatedField(required=True, slug_field='id', queryset=Movies.objects.filter(is_active=True))

    def validate_movie(self, movie):
        user = self.context.get('user')
        if UserWatchedMovie.objects.filter(user=user, movie=movie, is_active=True).exists():
            raise serializers.ValidationError(f"Movie {movie.name} already watched")
        return movie

    def create(self, validated_data):
        movie = validated_data.get('movie')
        user = self.context.get('user')
        obj, created = UserWatchedMovie.objects.get_or_create(user=user, movie=movie)
        if not created:
            obj.is_active = True
            obj.save()
        return obj

    def to_representation(self, obj):
        attr = super().to_representation(obj)
        attr.__setitem__('movie', MoviesSerializer(obj.movie).data)
        return attr

    class Meta:
        model = UserWatchedMovie
        fields = ("id", "movie")
