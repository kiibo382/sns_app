from django.contrib import admin
from .models import Post, Tag
# from django.contrib.auth.admin import UserAdmin

admin.site.register(Post)
admin.site.register(Tag)
