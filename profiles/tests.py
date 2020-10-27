from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Profile
from rest_framework.test import APIClient


User = get_user_model()


class ProfileTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='un1', password='pw1')
        self.user2 = User.objects.create_user(
            username='un2', password='pw2')

    def test_profile_created_via_signal(self):
        qs = Profile.objects.all()
        # TEST~~~
        self.assertEqual(qs.count(), 2)  # user1 & user2

    def test_following(self):
        first = self.user1
        second = self.user2
        first.profile.followers.add(second)  # user1 added user2 as a follower
        second_user_following_whom = second.rname_following.all()
        qs = second_user_following_whom.filter(user=first)
        # check user1 has not following anyone
        first_user_following_no_one = first.rname_following.all()
        # TEST~~~
        self.assertTrue(qs.exists())
        self.assertFalse(first_user_following_no_one.exists())

    def get_client(self):
        client = APIClient()
        client.login(username=self.user1.username, password='pw1')
        return client

    def test_follow_api_endpoint(self):
        client = self.get_client()
        response = client.post(
            f"/api/profiles/{self.user2.username}/follow",
            {"action": "follow"}
        )
        r_data = response.json()
        count = r_data.get("count")
        # TEST~~~
        self.assertEqual(count, 1)  # {"action": "follow"}

    def test_unfollow_api_endpoint(self):
        first = self.user1
        second = self.user2
        first.profile.followers.add(second)
        client = self.get_client()
        response = client.post(
            f"/api/profiles/{self.user2.username}/follow",
            {"action": "unfollow"}
        )
        r_data = response.json()
        count = r_data.get("count")
        # TEST~~~
        self.assertEqual(count, 0)  # {"action": "unfollow"}

    def test_cannot_follow_api_endpoint(self):
        client = self.get_client()  # client=user1
        response = client.post(
            # KO thể tự mình follow mình
            f"/api/profiles/{self.user1.username}/follow",
            {"action": "follow"}
        )
        r_data = response.json()
        count = r_data.get("count")
        # TEST~~~
        self.assertEqual(count, 0)
