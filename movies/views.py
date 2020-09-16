from itertools import islice

import requests
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from movies.models import *
from movies.serializers import (
    MoviesSerializer, MoviesFilterSet, MoviesCreateSerializer, UserWatchListMovieSerializer,
    CreateUserWatchListSerializer, UserWatchedMovieSerializer, CreateUserWatchedSerializer
)


class MoviesViewSet(viewsets.ModelViewSet):
    queryset = Movies.objects.all()
    # permission_classes = (IsAuthenticated,)
    http_method_names = ('post', 'get')
    filterset_class = MoviesFilterSet

    def get_serializer_class(self):
        serializer_class = MoviesSerializer
        if self.request.method == 'POST':
            serializer_class = MoviesCreateSerializer
        return serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            resp = requests.get(url)
            if resp.status_code != 200:
                return Response({"message": "Something went wrong"}, status=resp.status_code)
            soup = BeautifulSoup(resp.text, 'html.parser')
            movie_tbody = soup.find('tbody', class_='lister-list')
            movie_tbody_tr = movie_tbody.find_all('tr')
            if not movie_tbody_tr:
                return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
            movie_create_queries, movie_update_queries = list(), list()
            batch_size = 100
            for tr in movie_tbody_tr:
                name = tr.find("td", class_="titleColumn").a.text
                year = tr.find("td", class_="titleColumn").span.text
                rating_tag = tr.find("td", class_="ratingColumn imdbRating").strong
                rating = rating_tag.text if rating_tag else 0
                vote = tr.find("td", class_="posterColumn").find("span", attrs={'name': 'nv'})['data-value']
                director_star = tr.find("td", class_="titleColumn").a['title']

                try:
                    obj = Movies.objects.get(
                        name=name, released_year=int(year[1:5]), director_and_star=director_star)
                    obj.vote = vote
                    obj.rating = rating
                    obj.director_and_star = director_star
                    movie_update_queries.append(obj)
                except:
                    movie_create_queries.append(
                        Movies(name=name, released_year=int(year[1:5]), rating=rating, vote=vote,
                               director_and_star=director_star)
                    )

            start, stop = 0, batch_size
            while True:
                batch = list(islice(movie_update_queries, start, stop))
                if not batch:
                    break
                Movies.objects.bulk_update(batch, ["vote", "rating"], batch_size)
                start += batch_size
                stop += batch_size

            start, stop = 0, batch_size
            while True:
                batch = list(islice(movie_create_queries, start, stop))
                if not batch:
                    break
                Movies.objects.bulk_create(batch, batch_size)
                start += batch_size
                stop += batch_size
            return Response(status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserWatchListView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ('post', 'get', 'delete')
    model = UserWatchListMovie
    
    def get_serializer_class(self):
        serializer_class = UserWatchListMovieSerializer
        if self.request.method == 'POST':
            serializer_class = CreateUserWatchListSerializer
        return serializer_class

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, is_active=True).order_by('-created_at')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user})
        return context

    def destroy(self, request, *args, **kwargs):
        obj = get_object_or_404(self.get_queryset(), pk=kwargs.get('pk'))
        obj.is_active = False
        obj.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserWatchedView(UserWatchListView):
    model = UserWatchedMovie

    def get_serializer_class(self):
        serializer_class = UserWatchedMovieSerializer
        if self.request.method == 'POST':
            serializer_class = CreateUserWatchedSerializer
        return serializer_class
