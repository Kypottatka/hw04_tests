from django.contrib.auth import get_user_model
from django.test import TestCase
from django.conf import settings

from posts.models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Ф' * 100,
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Ф' * 100,
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        self.assertEqual(
            post.text[:settings.SYMBOLS_IN_STR],
            str(post)[:settings.SYMBOLS_IN_STR]
        ),
        group = PostModelTest.group
        self.assertEqual(group.title, str(group))

    def test_verbose_name(self):
        """Проверяем, что поля моделей Post, Group с verbose_name."""
        post = PostModelTest.post
        field_verboses = {
            'group': 'Группа',
            'text': 'Текст Поста',
            'author': 'Автор',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected
                ),
        group = PostModelTest.group
        field_verboses = {
            'title': 'Заголовок',
            'slug': 'Слаг в url-строке',
            'description': 'Описание',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).verbose_name, expected
                )

    def test_help_text(self):
        """Проверяем, что поля моделей Post, Group с help_text."""
        post = PostModelTest.post
        field_help_texts = {
            'group': 'Показывает название группы',
            'text': 'Введите текст Поста',
            'author': 'Показывает автора поста',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected
                ),

        group = PostModelTest.group
        field_help_texts = {
            'title': 'Укажите заголовок группы',
            'slug': 'Укажите название группы',
            'description': 'Введите описание группы',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    group._meta.get_field(value).help_text, expected
                )

    def test_group_title_max_length(self):
        """Проверяем, что длина поля title в модели Group не превышает 200."""
        group = PostModelTest.group
        max_length = group._meta.get_field('title').max_length
        self.assertEqual(max_length, 200)
