from datetime import date

from django.db import models
from django.shortcuts import reverse


class Category(models.Model):
    """ Category """

    name = models.CharField('Категория', max_length=150)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Actor(models.Model):
    """ Actor model """

    name = models.CharField('Имя', max_length=100)
    age = models.PositiveIntegerField('Возвраст', default=0)
    description = models.TextField('Описание')
    image = models.ImageField('Фото', upload_to='actors/')

    class Meta:
        verbose_name = 'Актер'
        verbose_name_plural = 'Актеры'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={
            "slug": self.name
        })


class Genre(models.Model):
    """ Genre model """

    name = models.CharField('Название', max_length=100)
    description = models.TextField('Описание')
    url = models.SlugField(max_length=160, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Movie(models.Model):
    """ Movie model """

    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    description = models.TextField('Описание')
    poster = models.ImageField('Постер', upload_to='movies/')
    year = models.PositiveSmallIntegerField('Дата выхода', default=2020)
    country = models.CharField('Страна', max_length=30)
    directors = models.ManyToManyField(Actor, verbose_name='Режиссер', related_name='film_director')
    actors = models.ManyToManyField(Actor, verbose_name='Актеры', related_name='film_actor')
    genres = models.ManyToManyField(Genre, verbose_name='Жанры')
    world_premiere = models.DateField('Премьера в мире', default=date.today)
    budget = models.PositiveIntegerField('Бюджет', default=0, help_text='Указать сумму в долларах')
    fees_in_usa = models.PositiveIntegerField(
        'Сборы в США', default=0, help_text='Указать сумму в долларах'
    )
    fees_in_world = models.PositiveIntegerField(
        'Сборы в мире', default=0, help_text='Указать сумму в долларах'
    )
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.SET_NULL, null=True,
    )
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField('Черновик', default=False)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    def get_review(self):
        return self.review_set.filter(parent__isnull=True)


class MovieShots(models.Model):
    """ Кадры из фильма """

    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField('Описание')
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name='Фильм', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Кадр из фильма'
        verbose_name_plural = 'Кадры из фильма'

    def __str__(self):
        return self.title


class RatingStar(models.Model):
    """ Звезда рейтинга """

    value = models.PositiveSmallIntegerField("Значение", default=0)

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'
        ordering = ('-value',)

    def __str__(self):
        return f'{self.value}'


class Rating(models.Model):
    """ Рейтинг """

    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда')
    movie = models.ForeignKey(
        Movie, on_delete=models.CASCADE, verbose_name='Фильм', related_name='ratings')

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class Review(models.Model):
    """ Отзыв """

    email = models.EmailField()
    name = models.CharField('Название', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL,
        blank=True, null=True, related_name='children'
    )
    movie = models.ForeignKey(
        Movie, verbose_name='Фильм', on_delete=models.CASCADE, related_name='reviews')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.name} - {self.movie}'
