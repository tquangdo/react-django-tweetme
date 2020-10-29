from django.contrib.auth import get_user_model
from rest_framework import authentication


User = get_user_model()


class DevAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        '''
        chú ý phải đúng id, nếu id KO tồn tại sẽ báo lỗi "KO có quyền like/unlike"
        '''
        qs = User.objects.filter(id=2)  # 2: trangia61, 3:dotq,...
        # qs = User.objects.all()
        user = qs.order_by("?").first()
        return (user, None)
