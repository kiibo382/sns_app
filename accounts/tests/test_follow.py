import pdb
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from friendship.models import Friend, Follow, FriendshipRequest
from accounts.views import follow, Info, accept, reject


class FollowSaveTests(TestCase):
    def test_follow_request(self):
        user = User.objects.create_user(username='test', password='test')
        other_user = User.objects.create_user(username='other', password='other')
        rf = RequestFactory()
        request = rf.post("/accounts/profile/2/follow/", data={'pk': other_user.id})
        request.user = user
        res=follow(request, other_user.id)
        # self.assertEqual(Friend.objects.sent_requests(user=user).count(), 1)
        self.assertEqual(res.status_code, 200)

    def test_accept(self):
        user = User.objects.create_user(username='test', password='test')
        other_user = User.objects.create_user(username='other', password='other')
        rf = RequestFactory()
        # request = rf.post("/accounts/profile/2/follow/", data={'pk': other_user.id})
        # request.user = user
        Friend.objects.add_friend(user, other_user)
        request = rf.post("/accounts/profile/2/info/accept/", data={'pk': other_user.id})
        request.user = other_user
        res=accept(request, user.id)
        self.assertEqual(res.status_code, 200)

    def test_reject(self):
        user = User.objects.create_user(username='test', password='test')
        other_user = User.objects.create_user(username='other', password='other')
        rf = RequestFactory()
        # request = rf.post("/accounts/profile/2/follow/", data={'pk': other_user.id})
        # request.user = user
        Friend.objects.add_friend(user, other_user)
        request = rf.post("/accounts/profile/2/info/reject/", data={'pk': other_user.id})
        request.user = other_user
        res=reject(request, user.id)
        self.assertEqual(res.status_code, 200)

    def test_accept_function(self):
        user = User.objects.create_user(username='test', password='test')
        other_user = User.objects.create_user(username='other', password='other')
        rf = RequestFactory()
        Friend.objects.add_friend(user, other_user)
        friend_request = FriendshipRequest.objects.get(to_user=other_user.id)
        friend_request.accept()
        self.assertTrue(Friend.objects.are_friends(user, other_user))

    def test_reject_function(self):
        user = User.objects.create_user(username='test', password='test')
        other_user = User.objects.create_user(username='other', password='other')
        rf = RequestFactory()
        Friend.objects.add_friend(user, other_user)
        friend_request = FriendshipRequest.objects.get(to_user=other_user.id)
        friend_request.reject()
        self.assertFalse(Friend.objects.are_friends(user, other_user))