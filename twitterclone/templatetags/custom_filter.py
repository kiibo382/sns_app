from django import template
from django.utils.safestring import mark_safe

from twitterclone.models import Like

register = template.Library()

@register.filter(name='get_likes')
def get_likes(like_posts, key):
    text = ""
    if key in like_posts:
        text = ""
        for like in like_posts[key]:
            text += f"{like.user.username}, "
            text += "がいいねしました"
    return text

@register.filter(name='is_like')
def is_like(post, user):
    if Like.objects.filter(user=user, post=post).exists():
        return mark_safe(f"<button class=\"like\" id=\"{post.id}\" type=\"submit\"><i class=\" fas fa-heart\"></i></button>")
    else:
        return mark_safe(f"<button class=\"like\" id=\"{post.id}\" type=\"submit\"><i class=\" far fa-heart\"></i></button>")