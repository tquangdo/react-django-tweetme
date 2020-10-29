from django.http import Http404
from django.shortcuts import render, redirect
from .models import Profile
from .forms import ProfileForm


def profile_update_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("/login?next=/profile/update")
    user = request.user
    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }
    my_profile = user.profile
    form = ProfileForm(request.POST or None,
                       instance=my_profile, initial=user_data)
    if form.is_valid():
        profile_obj = form.save(commit=False)
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email = form.cleaned_data.get('email')
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        profile_obj.save()
    context = {
        "form_from_viewspy": form,
        "btn_label_from_viewspy": "Save",
        "title_from_viewspy": "Update Profile"
    }
    return render(request, "profiles/form.html", context)


def profile_detail_view(request, username, *args, **kwargs):
    # user__username: vì profiles>models.py có column "user"
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        # access "profile/username" sẽ hiện 404 nếu profiles>models.py KO có Profile.objects.get_or_create()
        raise Http404
    profile_obj = qs.first()
    is_following = False
    if request.user.is_authenticated:
        user = request.user
        is_following = user in profile_obj.followers.all()
    context = {
        "profile_un_from_viewspy": username,
        "profile_from_viewspy": profile_obj,
        "is_following_from_viewspy": is_following
    }
    return render(request, "profiles/detail.html", context)
