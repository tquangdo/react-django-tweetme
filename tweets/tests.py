from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from .models import Tweet
User = get_user_model()


class TweetTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='un1', password='pw1')
        self.user2 = User.objects.create_user(
            username='un2', password='pw2')
        Tweet.objects.create(content="tweet1-1",
                             user=self.user1)
        Tweet.objects.create(content="tweet1-2",
                             user=self.user1)
        Tweet.objects.create(content="tweet2-1",
                             user=self.user2)
        self.currentCount = Tweet.objects.all().count()  # currentCount=3

    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content="tweet1-3",
                                         user=self.user1)
        # TEST~~~
        self.assertEqual(tweet_obj.id, 4)  # tweet1-1~1-3 & 2-1
        self.assertEqual(tweet_obj.user, self.user1)

    def get_client(self):
        client = APIClient()
        client.login(username=self.user1.username, password='pw1')
        return client

    def test_tweet_list(self):
        client = self.get_client()
        response = client.get("/api/tweets/")
        # TEST~~~
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)  # tweet1-1~1-3

    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action",
                               {"id": 1, "action": "like"})
        # TEST~~~
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 1)

    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action",
                               {"id": 2, "action": "like"})
        # TEST~~~
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/tweets/action",
                               {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)  # like + unlike=>0

    def test_action_retweet(self):
        client = self.get_client()
        response = client.post("/api/tweets/action",
                               {"id": 2, "action": "retweet"})
        # TEST~~~
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get("id")  # new_tweet_id=3+1=4
        self.assertNotEqual(2, new_tweet_id)
        self.assertEqual(self.currentCount + 1,
                         new_tweet_id)  # currentCount+1=3+1=new_tweet_id

    def test_tweet_create_api_view(self):
        request_data = {"content": "tweet1-4"}
        client = self.get_client()
        response = client.post("/api/tweets/create", request_data)
        # TEST~~~
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        new_tweet_id = response_data.get("id")  # new_tweet_id=4 ("tweet1-4")
        # currentCount+1=3+1=new_tweet_id
        self.assertEqual(self.currentCount + 1, new_tweet_id)

    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/tweets/1")  # "tweet1-1"
        # TEST~~~
        self.assertEqual(response.status_code, 200)
        data = response.json()
        _id = data.get("id")
        self.assertEqual(_id, 1)

    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete")  # "tweet1-1"
        # TEST~~~
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete")
        self.assertEqual(response.status_code, 404)
        response_incorrect_owner = client.delete(
            "/api/tweets/3/delete")  # "tweet2-1" của "un2" nhưng user="un1"
        self.assertEqual(response_incorrect_owner.status_code, 401)
