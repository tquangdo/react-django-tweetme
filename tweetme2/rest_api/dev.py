from django.contrib.auth import get_user_model
from rest_framework import authentication


User = get_user_model()


class DevAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        '''
        1/ chú ý phải đúng id, KO được id=1, nếu sai id sẽ báo lỗi "KO có quyền like/unlike"
        2/ khi đã bị lỗi KO có quyền mà mở browser localhost:8000 thì sẽ lỗi CORS
        '''
        qs = User.objects.filter(id=2)
        # qs = User.objects.all()
        user = qs.order_by("?").first()
        return (user, None)
