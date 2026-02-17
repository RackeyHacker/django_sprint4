from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from .constants import MAX_CHARFIELD_LENGTH, PREVIEW_TEXT_LENGTH
from .managers import PublishedPostQuerySet

User = get_user_model()


class CreatedAt(models.Model):
    created_at = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class IsPublishedCreatedAt(CreatedAt):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
    )

    class Meta(CreatedAt.Meta):
        abstract = True


class Category(IsPublishedCreatedAt):
    title = models.CharField(
        'Заголовок',
        max_length=MAX_CHARFIELD_LENGTH,
    )
    description = models.TextField('Описание',)
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; разрешены'
        'символы латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:PREVIEW_TEXT_LENGTH]


class Location(IsPublishedCreatedAt):
    name = models.CharField('Название места', max_length=MAX_CHARFIELD_LENGTH)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:PREVIEW_TEXT_LENGTH]


class Post(IsPublishedCreatedAt):
    title = models.CharField(
        'Заголовок',
        max_length=MAX_CHARFIELD_LENGTH,
    )
    text = models.TextField('Текст', )
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
        'можно делать отложенные публикации.'
    )
    image = models.ImageField(
        upload_to='images',
        blank=True,
        null=True,
        verbose_name='Фото',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(

        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name='Категория'
    )

    objects = PublishedPostQuerySet.as_manager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'post_id': self.pk})

    def __str__(self):
        return self.title[:PREVIEW_TEXT_LENGTH]


class Comment(CreatedAt):
    text = models.TextField('Текст коммeнтария')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('created_at',)

    def __str__(self):
        return self.title[:PREVIEW_TEXT_LENGTH]
