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
        self.assertEqual(res.status_code, 200)
        Friend.objects.add_friend(user, other_user)
        self.assertTrue(FriendshipRequest.objects.get(to_user=other_user.id))
        friend_request = FriendshipRequest.objects.get(to_user=other_user.id)
        friend_request.cancel()
        try:
            fri_req=FriendshipRequest.objects.get(to_user=other_user.id)
        except:
            fri_req=None
        self.assertEqual(fri_req, None)

    def test_accept_and_cancel_follow(self):
        user = User.objects.create_user(username='test', password='test')
        other_user = User.objects.create_user(username='other', password='other')
        rf = RequestFactory()
        Friend.objects.add_friend(user, other_user)
        request = rf.post("/accounts/profile/2/info/accept/", data={'pk': other_user.id})
        request.user = other_user
        res=accept(request, user.id)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(Friend.objects.are_friends(user, other_user))
        Friend.objects.remove_friend(user, other_user)
        self.assertFalse(Friend.objects.are_friends(user, other_user))


    def test_reject(self):
        user = User.objects.create_user(username='test', password='test')
        other_user = User.objects.create_user(username='other', password='other')
        rf = RequestFactory()
        Friend.objects.add_friend(user, other_user)
        request = rf.post("/accounts/profile/2/info/reject/", data={'pk': other_user.id})
        request.user = other_user
        res=reject(request, user.id)
        self.assertEqual(res.status_code, 200)
        self.assertFalse(Friend.objects.are_friends(user, other_user))

    def test_accept_function(self):
        user = User.objects.create_user(username='test', password='test')
        other_user = User.objects.create_user(username='other', password='other')
        Friend.objects.add_friend(user, other_user)
        friend_request = FriendshipRequest.objects.get(to_user=other_user.id)
        friend_request.accept()
        self.assertTrue(Friend.objects.are_friends(user, other_user))

    def test_reject_function(self):
        user = User.objects.create_user(username='test', password='test')
        other_user = User.objects.create_user(username='other', password='other')
        Friend.objects.add_friend(user, other_user)
        friend_request = FriendshipRequest.objects.get(to_user=other_user.id)
        friend_request.reject()
        self.assertFalse(Friend.objects.are_friends(user, other_user))