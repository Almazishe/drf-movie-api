from django.db import models

from rest_framework import generics, permissions

from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Review, Actor
from .services import get_client_ip, MovieFilter
from .serializers import (
    ActorListSerializer, ReviewSerializer,
    CreateRatingSerializer, ReviewCreateSerializer,
    MovieListSerializer, MovieDetailSerializer,
    ActorDetailSerializer
)


class MovieListView(generics.ListAPIView):
    """ Вывод списка фильмов """

    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings',
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        print(movies)
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """ Вывод информации фильма """

    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer

class ReviewCreateView(generics.CreateAPIView):
    """ Создание отзыва """

    serializer_class = ReviewCreateSerializer

class AddStarRatingView(generics.CreateAPIView):
    """ Добавление рейтинга """

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))

class ActorsListView(generics.ListAPIView):
    """ Вывод списка актеров """

    queryset =  Actor.objects.all()
    serializer_class = ActorListSerializer

class ActorsDetailView(generics.RetrieveAPIView):
    """ Вывод списка актеров """

    queryset =  Actor.objects.all()
    serializer_class = ActorDetailSerializer

