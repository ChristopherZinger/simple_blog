from django.db import models
from post.models import Post, Images


class Tag(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    post = models.ManyToManyField(
        Post, related_name='tags',
        )
    image = models.ManyToManyField(
        Images, related_name='tags',
        )
