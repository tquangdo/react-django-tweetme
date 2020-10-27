from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include  # url()
from django.views.generic import TemplateView

from accounts.views import (
    login_view,
    logout_view,
    register_view,
)

from tweets.views import (
    # home_view,
    tweets_list_view,
    tweets_detail_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', home_view),
    path('', tweets_list_view),
    path('<int:tweet_id>', tweets_detail_view),
    path('api/tweets/', include('tweets.api.urls')),
    path('react', TemplateView.as_view(
        template_name='react.html')),  # react_via_dj.html
    path('login', login_view),
    path('logout', logout_view),
    path('register', register_view),
    # vì là regular expression nên URL vầy vẫn chạy: profile/trangia61
    re_path(r'profiles?/', include('profiles.urls')),
    re_path(r'api/profiles?/', include('profiles.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
