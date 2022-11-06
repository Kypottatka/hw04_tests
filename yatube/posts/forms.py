from posts.models import Post

from django.forms import ModelForm


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = (
            'text',
            'group',
        )
        labels = {
            'text': 'Текст статьи',
            'group': 'Группа',
        }
        help_texts = {
            'text': 'обязательное поле',
            'group': 'Выберите группу',
        }
