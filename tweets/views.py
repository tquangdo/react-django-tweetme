import random
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .models import Tweet
from .forms import TweetForm

# ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    # print(args, kwargs)
    # -> nếu "urls.py" >path('<int:tweet_id>', home_view) thì print hiện: {'tweet_id',123}
    return render(request, "pages/feed.html")


def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)
    if form.is_valid():
        messages.info(request, 'Đã tạo tweet mới OK!')
        obj = form.save(commit=False)
        # do other form related logic
        obj.save()
        form = TweetForm()  # reset lại form mới
    return render(request, 'components/form.html',
                  context={"formTweetCreateView": form})


def tweets_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [{'id': x.id, 'content': x.content,
                    "likes": random.randint(0, 99)} for x in qs]
    data = {
        'responseFromTListView': tweets_list
    }
    return JsonResponse(data)
    # return render(request, "tweets/list.html")


def tweets_detail_view(request, tweet_id, *args, **kwargs):
    # 1/dùng cmt shell INS obj.content = 'Hello world'
    # 2/
    # data = {
    #     'id': tweet_id,
    # }
    # status = 200
    # try:
    #     obj = Tweet.objects.get(id=tweet_id)
    #     data['content'] = obj.content
    # except:
    #     data['msg'] = 'NOT found'
    #     status = 404
    # # KO được code tắt: JsonResponse(data, status)
    # return JsonResponse(data, status=status)
    #     raise Http404
    # return HttpResponse(f"Hello {tweet_id} - {obj.content}")
    return render(request, "tweets/detail.html", context={"tweet_id": tweet_id})
