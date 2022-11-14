import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Group, Post


User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TaskCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='тестовое описание группы'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверка создания поста
    def test_create_post(self):
        '''Проверка создания нового поста'''
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        post = Post.objects.get(id=1)
        self.assertTrue(post)
        self.assertEqual(self.user, post.author)
        self.assertEqual(self.group.id, post.group.id)
        self.assertRedirects(
            response,
            reverse('posts:profile',
                    kwargs={'username': self.user.username}
                    )
        )

        for field in form_data:
            if field == 'group':
                self.assertEqual(
                    form_data[field],
                    self.group.id)
            else:
                self.assertEqual(
                    form_data[field], getattr(response.context['post'], field)
                )

    # Проверка редактирования поста
    def test_edit_post(self):
        form_data = {
            'text': 'Тестовый текст',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}),
            data=form_data,
            follow=True
        )
        post = Post.objects.get(id=1)
        self.assertTrue(post)
        self.assertEqual(self.user, post.author)
        self.assertEqual(self.group.id, post.group.id)
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}))

        for field in form_data:
            if field == 'group':
                self.assertEqual(
                    form_data[field],
                    post.group.id)
            else:
                self.assertEqual(
                    form_data[field], post.text
                )
