from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# Function based views to Class Based Views


def login_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user_ = form.get_user()
        login(request, user_)
        return redirect("/")
    context = {
        "form_from_viewspy": form,
        "btn_label_from_viewspy": "Login",
        "title_from_viewspy": "Login"
    }
    return render(request, "accounts/auth.html", context)


def logout_view(request, *args, **kwargs):
    if request.method == "POST":
        logout(request)
        return redirect("/login")
    context = {
        "form_from_viewspy": None,
        "description_from_viewspy": "Are you sure you want to logout?",
        "btn_label_from_viewspy": "Click to Confirm",
        "title_from_viewspy": "Logout"
    }
    return render(request, "accounts/auth.html", context)


def register_view(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=True)
        user.set_password(form.cleaned_data.get("password1"))
        # send a confirmation email to verify their account
        login(request, user)
        return redirect("/")
    context = {
        "form_from_viewspy": form,
        "btn_label_from_viewspy": "Register",
        "title_from_viewspy": "Register"
    }
    return render(request, "accounts/auth.html", context)
