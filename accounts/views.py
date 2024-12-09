from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    # 获取当前用户及其关联的个人信息
    user_profile = request.user.profile  # 如果是自定义 User 模型，则直接访问扩展字段
    context = {
        'username': request.user.username,
        'avatar': user_profile.avatar.url if user_profile.avatar else None,
        'bio': user_profile.bio,
        'personal_experience': user_profile.personal_experience,
        'skills': user_profile.skills.split(',') if user_profile.skills else [],
    }
    return render(request, 'home.html', context)
