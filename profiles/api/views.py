import random
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import Profile
from ..serializers import PublicProfileSerializer

User = get_user_model()
ALLOWED_HOSTS = settings.ALLOWED_HOSTS


@api_view(['GET'])
def profile_detail_api_view(request, username, *args, **kwargs):
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        return Response({"detail": "User not found"}, status=404)
    profile_obj = qs.first()
    data = PublicProfileSerializer(instance=profile_obj)
    return Response(data.data, status=200)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
# "username" lấy từ urls.py > '<str:username>/follow'
def user_follow_view(request, username, *args, **kwargs):
    me = request.user
    other_user_qs = User.objects.filter(
        username=username)  # 1/datatype "other_user_qs" là "User" model
    if me.username == username:
        my_followers = me.profile.followers.all()  # A) me.profile
        return Response({"count": my_followers.count()}, status=200)
    if not other_user_qs.exists():
        return Response({}, status=404)
    other = other_user_qs.first()
    profile = other.profile  # 2/datatype "profile" là "Profile" model
    data = request.data or {}
    action = data.get("action")
    if action == "follow":
        # 3/trong "Profile" model có column "followers"
        profile.followers.add(me)
    elif action == "unfollow":
        profile.followers.remove(me)
    else:
        pass
    current_followers_qs = profile.followers.all()  # B) other.profile
    return Response({"count": current_followers_qs.count()}, status=200)
