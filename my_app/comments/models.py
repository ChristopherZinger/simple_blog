from django.db import models
from post.models import Post
from accounts.models import User



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    publication_date =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'by: {}. post id {},'.format(self.author, self.post.id)
