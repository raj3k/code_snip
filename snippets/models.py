from django.db import models
from django.conf import settings
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    #     id UUID
    user = models.ForeignKey(
        settings.USER_AUTH_MODEL,
        related_name='snippets_created',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=200,
        blank=True
    )
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(
        choices=LANGUAGE_CHOICES,
        default='python',
        max_length=100
    )
    style = models.CharField(
        choices=STYLE_CHOICES,
        default='friendly',
        max_length=100
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created'])
        ]
        ordering = ['-created']

    def __str__(self):
        return self.title
