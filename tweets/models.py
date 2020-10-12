from django.db import models


class Tweet(models.Model):
    # parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    # # many users can many tweets
    # user = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name="tweets")
    # likes = models.ManyToManyField(
    #     User, related_name='tweet_user', blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # objects = TweetManager()
    # # def __str__(self):
    # #     return self.content

    # class Meta:
    #     ordering = ['-id']

    # @property
    # def is_retweet(self):
    #     return self.parent != None

    # def serialize(self):
    #     '''
    #     Feel free to delete!
    #     '''
    #     return {
    #         "id": self.id,
    #         "content": self.content,
    #         "likes": random.randint(0, 200)
    #     }
