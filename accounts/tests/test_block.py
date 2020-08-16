from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from friendship.models import Friend, Follow, Block, FriendshipRequest
from accounts.views import block, Info

class FollowSaveTests(TestCase):
    def test_block(self):
        user = User.objects.create_user(username='test', password='test')
        other_user = User.objects.create_user(username='other', password='other')
        rf = RequestFactory()
        request = rf.post("/accounts/profile/2/block/", data={'pk': other_user.id})
        request.user = user
        res=block(request, other_user.id)
        self.assertEqual(res.status_code, 200)

    def test_block_function(self):
        user = User.objects.create_user(username='test', password='test')
        other_user = User.objects.create_user(username='other', password='other')
        rf = RequestFactory()
        Friend.objects.add_friend(user, other_user)
        Block.objects.add_block(other_user, user)
        self.assertTrue(Block.objects.is_blocked(other_user, user))
        Block.objects.remove_block(other_user, user)
        self.assertFalse(Block.objects.is_blocked(other_user, user))