from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import pgettext_lazy
from ckeditor.fields import RichTextField



CATEGORY_CHOICES = {('TANKS', 'Танки'),
                    ('HEALERS', 'Хилы'),
                    ('DD', 'ДД'),
                    ('VENDORS', 'Торговцы'),
                    ('GUILD_MATERS', 'Гилдмастеры'),
                    ('QUEST_GIVERS', 'Квестгиверы'),
                    ('BLACKSMITHS', 'Кузнецы'),
                    ('SKINNERS', 'Кожевники'),
                    ('POTION_MASTERS', 'Зельевары'),
                    ('SPELL_MASTERS', 'Мастера заклинаний')}


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author')
    category = models.CharField(max_length=28, choices=CATEGORY_CHOICES, default='Tanks', verbose_name='category')
    dateCreation = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128, verbose_name=pgettext_lazy('post title', 'title'))
    text = RichTextField()

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'{self.pk}'

    class Meta:
        ordering = ['id']


class Comment(models.Model):
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_dateCreation = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def get_absolute_url(self):
        return f'{self.pk}'

    class Meta:
        ordering = ['id']