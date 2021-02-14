import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Tag(models.Model):
    tag = models.CharField('タグ名', max_length=50)

    def __str__(self):
       return self.tag

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    text = models.TextField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    tag = models.ForeignKey(Tag, verbose_name='タグ', on_delete=models.PROTECT)
    like_num = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.text

    def was_published_recently(self):
        return self.published_date >= timezone.now() - datetime.timedelta(days=1)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)