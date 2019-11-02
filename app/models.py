from django.db import models
from django.contrib.auth.models import User


# Categoryモデルを作成
class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Photo(models.Model):
    title = models.CharField(max_length=150)
    comment = models.TextField(blank=True)
    image = models.ImageField(upload_to = 'photos')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    like_num = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Contact(models.Model):
    title = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    photos = models.ForeignKey(Photo, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.follower.username, self.following.username)