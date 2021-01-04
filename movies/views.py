from django.shortcuts import get_object_or_404
from django.db import models

from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import generics, permissions, viewsets

from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Review, Actor
from .services import get_client_ip, MovieFilter, PaginationMovies
from .serializers import (
    ActorListSerializer, ReviewSerializer,
    CreateRatingSerializer, ReviewCreateSerializer,
    MovieListSerializer, MovieDetailSerializer,
    ActorDetailSerializer
)


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """ Вывод списка или информации фильма """

    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    pagination_class = PaginationMovies

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count('ratings',
                                     filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """ Добавление отзыва к фильму """

    serializer_class = ReviewCreateSerializer

class AddStartRatingViewSet(viewsets.ModelViewSet):
    """ Добавление рейтинга к фильму """

    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))



class ActorViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSerializer
        elif self.action == 'retrieve':
            return ActorDetailSerializer



# class MovieListView(generics.ListAPIView):
#     """ Вывод списка фильмов """

#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = MovieFilter
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_queryset(self):
#         movies = Movie.objects.filter(draft=False).annotate(
#             rating_user=models.Count('ratings',
#                                      filter=models.Q(ratings__ip=get_client_ip(self.request)))
#         ).annotate(
#             middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
#         )
#         print(movies)
#         return movies


# class MovieDetailView(generics.RetrieveAPIView):
#     """ Вывод информации фильма """

#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer

# class ReviewCreateView(generics.CreateAPIView):
#     """ Создание отзыва """

#     serializer_class = ReviewCreateSerializer

# class AddStarRatingView(generics.CreateAPIView):
#     """ Добавление рейтинга """

#     serializer_class = CreateRatingSerializer

#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))

# class ActorsListView(generics.ListAPIView):
#     """ Вывод списка актеров """

#     queryset =  Actor.objects.all()
#     serializer_class = ActorListSerializer

# class ActorsDetailView(generics.RetrieveAPIView):
#     """ Вывод списка актеров """

#     queryset =  Actor.objects.all()
#     serializer_class = ActorDetailSerializer

