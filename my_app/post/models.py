from django.db import models
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
# Create your models here.

class Images(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='post_images/')

    def __str__(self):
        return str(self.post.title) + ' - image.'

class PostSeries(models.Model):
    '''
    this is a class to gather seriest of posts that relates to each other
    and should be readed in perticular. order.
    '''
    title = models.CharField(max_length=255)
    slug =  models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Topic(models.Model):
    # Topic is a way to divide posts into categories that will be chosable in main menu
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to='topic_images/')

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=128, unique=True)
    subtitle = models.CharField(max_length=128)
    description = models.CharField(max_length=512)
    publication_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    is_published = models.BooleanField(default=False, blank=True, null=True)
    post_series = models.ForeignKey(
            PostSeries, on_delete=models.CASCADE,
            related_name='posts', null=True,
            blank=True,
        )
    topic = models.ForeignKey(
            Topic, on_delete=models.CASCADE,
            related_name='posts',
        )

    class Meta:
        ordering = ['-publication_date']

    def __str__(self):
        return self.title



def folder_path(instance, filename):
    import os
    return os.path.join('post_images/',instance.post.slug, filename)

class PostSection(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='sections'
        )
    text = models.TextField()
    image = models.ImageField(upload_to=folder_path)
    order = models.IntegerField()
    tag = models.CharField(max_length=255, default='<p>')

    def __str__(self):
        return 'post: {}, item: {}'.format(self.post, self.id)

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "{}-{}".format(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_reciver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_reciver, sender=Post)
