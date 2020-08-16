from django.contrib.auth.models import User
from django.test import TestCase
from twitterclone.models import Post, Tag, Like


class TagAssertion(TestCase):
    def assertTagModel(self, actual_tag, tag):
        self.assertEqual(actual_tag.tag, tag)

class PostAssertion(TestCase):
    def assertPostModel(self, actual_post, author, text, tag):
        self.assertEqual(actual_post.author, author)
        self.assertEqual(actual_post.text, text)
        self.assertEqual(actual_post.tag, tag)

class LikeAssertion(TestCase):
    def assertLikeModel(self, actual_post,like, user):
        self.assertEqual(like.user, user)
        self.assertEqual(like.post, actual_post)
        # self.assertEqual(actual_post.like_num, like_num)

class TagModelTests(TagAssertion):
    def test_is_empty(self):
        saved_tags = Tag.objects.all()
        self.assertEqual(saved_tags.count(), 0)

    def test_is_not_empty(self):
        tag = Tag()
        tag.save()
        saved_tags = Tag.objects.all()
        self.assertEqual(saved_tags.count(), 1)

    def test_saving_and_retrieving_tag(self):
        tag = Tag()
        tag.tag = 'tag'
        tag.save()
        saved_tags = Tag.objects.all()
        actual_tag = saved_tags[0]

        self.assertTagModel(actual_tag, tag.tag)

class PostModelTests(PostAssertion):
    def creating_a_post_and_saving(self, author=None, text=None, tag=None):
        post = Post()
        if author is not None:
            post.author = author
        if text is not None:
            post.text = text
        if tag is not None:
            post.tag = tag
        post.save()

    def test_is_empty(self):
        saved_posts = Post.objects.all()
        self.assertEqual(saved_posts.count(), 0)

    def test_saving_and_retrieving_post(self):
        author = User()
        author.username='author'
        author.password='password'
        author.save()
        text ='text'
        tag = Tag()
        tag.tag = 'tag'
        tag.save()
        self.creating_a_post_and_saving(author, text, tag)

        saved_posts = Post.objects.all()
        actual_post = saved_posts[0]

        self.assertPostModel(actual_post, author, text, tag)

class LikeModelTests(LikeAssertion):

    def test_add_like(self):
        user = User()
        user.username = "username"
        user.password = "password"
        user.save()
        tag = Tag()
        tag.tag = 'tag'
        tag.save()
        post = Post()
        post.author=user
        post.text = "text"
        post.tag = tag
        post.save()
        like = Like()
        like.user = user
        like.post = post
        like.save()

        self.assertLikeModel(post, like, user)