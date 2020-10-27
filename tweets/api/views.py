from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
'''
chú ý: "from .."
'''
from ..models import Tweet
from ..forms import TweetForm
from ..serializers import (
    TweetSerializer,
    TweetActionSerializer,
    TweetCreateSerializer,
)
ALLOWED_HOSTS = settings.ALLOWED_HOSTS


# ~~~~~~~~~~~~~~~ create bằng Serializer (rest FW) ~~~~~~~~~~~~~~~
@api_view(['POST'])
# @authentication_classes([SessionAuthentication, MyCustomAuth])
@permission_classes([IsAuthenticated])
# dòng code trên thay cho đống code của pure_django: if not userVar.is_authenticated
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Reponse({}, status=404)
    obj = qs.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this tweet"}, status=401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Tweet deleted"}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    '''
    1/phải truyền args (id, action...) thông qua TweetActionSerializer mà KO truyền direct trong (request, *args, **kwargs) vì khi user like/unlike liên tục sẽ ảnh hưởng performance
    2/id is required.
    3/action options are: like, unlike, retweet
    '''
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id_serialize = data.get("id")
        action_serialize = data.get("action")
        content_serialize = data.get("content")
        qs = Tweet.objects.filter(id=tweet_id_serialize)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action_serialize == "like":
            # đã test trước trên shell, 1 user chỉ được like 1 lần
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action_serialize == "unlike":
            obj.likes.remove(request.user)  # đã test trước trên shell
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action_serialize == "retweet":
            new_tweet = Tweet.objects.create(
                user=request.user,
                parent=obj,
                content=content_serialize,
            )
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
    return Response({}, status=200)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    username = request.GET.get('username')  # ?username=dotq
    if username != None:
        qs = qs.filter(user__username__iexact=username)
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)


# ~~~~~~~~~~~~~~~ create bằng forms.py ~~~~~~~~~~~~~~~
def tweet_create_view_pure_django(request, *args, **kwargs):
    userVar = request.user
    if not userVar.is_authenticated:
        userVar = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    # print(xxx)  # test alert("There was a server error, please try again.")
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next-from-feed-html") or None
    if form.is_valid():
        obj = form.save(commit=False)
        # do other form related logic
        obj.user = userVar
        obj.save()
        # C1
        if request.is_ajax():
            # 201 == created items
            # tweet_create_view_pure_django() dc thay bằng tweet_create_view() nên ko gọi obj.serialize() nữa => ko còn random số likes nữa!
            return JsonResponse(obj.serialize(), status=201)
        # C2
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        # C3
        form = TweetForm()  # reset lại form mới
        messages.info(request, 'Đã tạo tweet mới OK!')
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html',
                  context={"formTweetCreateView": form})


def tweets_list_view_pure_django(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweets_list = [x.serialize() for x in qs]
    data = {
        'responseFromTListView': tweets_list
    }
    return JsonResponse(data)
    # return render(request, "tweets/list.html")


def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
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
