from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include  # url()
from django.views.generic import TemplateView

# from accounts.views import (
#     login_view,
#     logout_view,
#     register_view,
# )

from tweets.views import (
    home_view,
    tweets_list_view,
    tweet_detail_view,
)

urlpatterns = [
    path('', home_view),
    path('admin/', admin.site.urls),
    path('tweets', tweets_list_view),
    path('tweets/<int:tweet_id>', tweet_detail_view),
    path('api/tweets/', include('tweets.urls')),
    path('react', TemplateView.as_view(template_name='react.html')),
    # path('react', TemplateView.as_view(template_name='react_via_dj.html')),
    # path('login/', login_view),
    # path('logout/', logout_view),
    # path('register/', register_view),
    # re_path(r'profiles?/', include('profiles.urls')),
    # re_path(r'api/profiles?/', include('profiles.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
