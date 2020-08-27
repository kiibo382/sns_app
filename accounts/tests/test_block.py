from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from friendship.models import Friend, Follow, Block, FriendshipRequest
from accounts.views import block, Info

class FollowSaveTests(TestCase):
    def test_block(self):
        user = User.objects.create_user(username='test', password='test')
        other_user = User.objects.create_user(username='other', password='other')

        rf = RequestFactory()
        request = rf.post("/accounts/profile/2/", data={'block': ''})
        request.user = user
        res=block(request, other_user.id)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Block.objects.is_blocked(user, other_user))

        request = rf.post("/accounts/profile/2/", data={'remove_block': ''})
        request.user = user
        res = block(request, other_user.id)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Block.objects.is_blocked(user, other_user))
