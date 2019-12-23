from django.contrib import admin

from django.contrib import admin
from .models import Post, Images, PostSeries, Topic, PostSection
# Register your models here.

admin.site.register(Post)
admin.site.register(PostSeries)
admin.site.register(Topic)
admin.site.register(Images)
admin.site.register(PostSection)
