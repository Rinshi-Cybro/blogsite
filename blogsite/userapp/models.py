from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogModel(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    image=models.ImageField(upload_to='blog_images',null=True,blank=True)
    date=models.DateField(null=True,auto_now_add=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')
    liked_by=models.ManyToManyField(User)

    @property
    def liked_count(self):
        liked_cnt=self.liked_by.all().count()
        return liked_cnt


class Comments(models.Model):
    date=models.DateField(null=True,auto_now_add=True)
    comment=models.TextField()
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    blog=models.ForeignKey(BlogModel,on_delete=models.CASCADE,related_name='blog')     
