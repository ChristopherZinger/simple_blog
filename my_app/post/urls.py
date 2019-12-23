
from django.urls import path
from . views import (
post_create, post_update,
post_delete, post_detail,
post_publish,
post_list, post_list_all,
post_republish, post_take_down,
) #PostDeleteView, PostDetailView, PostUpdateView


app_name = 'post'

urlpatterns = [
    path('create/', post_create, name='post_create'),
    path('update/<int:post_id>/', post_update, name='post_update'),
    path('delete/<int:post_id>/', post_delete, name='post_delete'),
    path('post_list_all/', post_list_all, name='post_list_all'),
    path('<slug:slug>/', post_detail, name='post_detail'),

    path('post_republish/<int:post_id>/', post_republish, name='post_republish'),
    path('post_take_down/<int:post_id>/', post_take_down, name='post_take_down'),
 ]
