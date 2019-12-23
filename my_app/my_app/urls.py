from django.contrib import admin
from django.urls import path, include
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import TemplateView
from post.views import post_list




urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('profile/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    #posts
    path('post/', include('post.urls')),
    path('', post_list, name='index'),
    path('tags/', include('tags.urls')),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
