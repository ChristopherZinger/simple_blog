from django.urls import path
from . views import (
tag_create, tag_detail,
tag_list, tag_update,
tag_delete, add_tag_to_post,
remove_tag_from_post,
)


app_name='tags'

urlpatterns = [
    path('create', tag_create, name='tag_create'),
    path('list', tag_list, name='tag_list'),
    path('<slug:slug>', tag_detail, name='tag_detail'),
    path('update/<int:tag_id>/', tag_update, name='tag_update'),
    path('delete/<int:tag_id>/', tag_delete, name='tag_delete'),
    path(
        'add_tag_to_post/<int:post_id>/<int:tag_id>/',
        add_tag_to_post,
        name='add_tag_to_post'
    ),
    path(
        'remove_tag_from_post/<int:post_id>/<int:tag_id>/',
        remove_tag_from_post,
        name='remove_tag_from_post'
    ),
]
