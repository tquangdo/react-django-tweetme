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
    # đang chạy với build static of tweetme2-web(public>index.html) có data-username="trangia61"
    # login với acc="dotq" rồi access "localhost:8000" thì dù "dotq" có tweets nhưng UI KO hiện!!!
    # lí do: vẫn đang chạy với build static of tweetme2-web có data-username="trangia61":
    # tweets_list_view > list.html > base.html > {% include 'react/js.html' %}
    # => muốn phản ánh thì phải sửa bên tweetme2-web: npm run build rồi copy paste qua!
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
