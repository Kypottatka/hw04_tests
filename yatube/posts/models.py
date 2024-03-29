from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Заголовок',
        help_text='Укажите заголовок группы'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг в url-строке',
        help_text='Укажите название группы'
    )
    description = models.TextField(
        verbose_name='Описание',
        help_text='Введите описание группы'
    )

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    SYMBOLS_IN_STR = 15

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    text = models.TextField(
        verbose_name='Текст Поста',
        help_text='Введите текст Поста'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата Публикации',
        help_text='Покаазывает дату публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор',
        help_text='Показывает автора поста'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Группа',
        help_text='Показывает название группы'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True
    )

    def __str__(self):
        return self.text[self.SYMBOLS_IN_STR]

    class Meta:
        ordering = ('-pub_date',)
