from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myapp'
    def ready(self):
        import myapp.signals  # 确保信号注册
        from django.contrib.auth.models import User
        from myapp.models import UserProfile  # 替换为你的实际路径

        # 自动为缺失的用户创建 profile
        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user)
