import random
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    # -> nếu "urls.py" >path('<int:tweet_id>', home_view) thì print(args, kwargs) hiện: {'tweet_id',123}
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    return render(request, "pages/feed.html", context={"username": username}, status=200)


def tweets_list_view(request, *args, **kwargs):
    return render(request, "tweets/list.html")


def tweets_detail_view(request, tweet_id, *args, **kwargs):
    return render(request, "tweets/detail.html", context={"tweet_id_from_viewspy": tweet_id})
