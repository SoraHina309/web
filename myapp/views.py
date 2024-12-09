import os
import json
from bson import ObjectId
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from pymongo import MongoClient
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseForbidden
from .models import Skill, Project, Contact, UserProfile
from .db_module import MyMongodb
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from .forms import AvatarUploadForm


def home(request):
    return render(request, 'base.html')

def personal_detail(request):
    return render(request, 'personal_detail.html')

def personal_experience(request):
    return render(request, 'personal_experience.html')

def skills(request):
    return render(request, 'skills.html')

def contact(request):
    return render(request, 'contact.html')


db=MyMongodb('resume')

#动态加载
MARKDOWN_DIR = os.path.join(settings.BASE_DIR, 'markdown_files')

def get_markdown_content(file_name):
    """
    读取指定 Markdown 文件内容
    """
    file_path = os.path.join(MARKDOWN_DIR, file_name)

    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def api_home_markdown(request):
    """
    返回 Home Page 的 Markdown 数据
    """
    content = get_markdown_content('home.md')
    return JsonResponse({'markdown': content}, safe=False)

def api_personal_detail_markdown(request):
    """
    返回 Personal Detail 的 Markdown 数据
    """
    content = get_markdown_content('personal_detail.md')
    return JsonResponse({'markdown': content}, safe=False)

def api_hobbies_markdown(request):
    """
    返回 Personal Detail 的 Markdown 数据
    """
    content = get_markdown_content('hobbies.md')
    return JsonResponse({'markdown': content}, safe=False)

def api_skills(request):
    """
    返回 Skills 数据
    """
    skills = db.get_skills('skills')
    return JsonResponse({'skills': skills}, safe=False)

def api_personal_experience(request):
    """
    返回 Projects 数据（与 Personal Experience 对应）
    """
    projects = db.get_projects('projects')
    return JsonResponse({'projects': projects}, safe=False)

def api_contact(request):
    """
    返回 Contact 数据
    """
    contact = db.get_contact('contact')
    return JsonResponse(contact, safe=False)

def personal_experience_list_view(request):
    # 获取 Markdown 文件目录下的所有文件名
    base_dir = 'markdown_files/personal_experience/'
    projects = [f.split('.')[0] for f in os.listdir(base_dir) if f.endswith('.md')]

    return JsonResponse({'projects': [{'name': p} for p in projects]})

def personal_experience_detail_view(request, project_name):
    file_path = f'markdown_files/personal_experience/{project_name}.md'

    try:
        with open(file_path, 'r') as file:
            markdown_content = file.read()
        return HttpResponse(markdown_content, content_type='text/plain')
    except FileNotFoundError:
        raise Http404(f"Markdown file for {project_name} not found.")


comments_data = {}

def user_status_view(request):
    if request.user.is_superuser:
        return JsonResponse({'is_authenticated': request.user.is_authenticated,'is_admin':request.user.is_superuser})
    return JsonResponse({'is_authenticated': request.user.is_authenticated})

# def upload_image(request):
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return render(request, 'success.html')
#     else:
#         form = ImageForm()
#     return render(request, 'upload.html', {'form': form})



@csrf_protect
@login_required
def submit_comment_view(request, project_name):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            rating = int(data.get('rating', 5))
            text = data.get('text', '')
            # 添加评论
            comment = {
                "project_name": project_name,
                "name": request.user.username,
                "rating": rating,
                "text": text
            }
            db.insert_comment('comments',comment)
            return JsonResponse({'message': 'Comment added successfully!'},status=201)

        except Exception as e:
            print(f"Unexpected Error: {e}")
            return JsonResponse({'error': str(e)}, status=400)
    else:
        return HttpResponseForbidden('Invalid request method.')
    
def get_comments_view(request, project_name):
    current_user = request.user
    per_page = int(request.GET.get('per_page', 5))
    page = int(request.GET.get('page', 1))
    skip = (page - 1) * per_page
    total_comments = db.count_documents('comments', project_name)
    comments = list(db.find_data('comments',{'project_name':project_name}).skip(skip).limit(per_page))
    comments_data = [
            {
                'id': str(comment['_id']),
                'project_name':comment['project_name'],
                'user': comment['name'],
                'rating': comment['rating'],
                'text': comment['text'],
            }
            for comment in comments
        ]
    return JsonResponse({'comments': comments_data,
            'total_comments': total_comments,
            'page': page,
            'total_pages': (total_comments + per_page - 1)//per_page,
            "current_user": current_user.username,
            })

@csrf_protect
@login_required
def delete_comment_view(request, project_name, comment_id):
    if request.method == "DELETE":
        # 查找评论
        from bson import ObjectId
        comment = db.find_data('comments', {"_id": ObjectId(comment_id)})
        if not comment:
            return JsonResponse({"error": "Comment not found"}, status=404)
        # 检查权限：只有管理员或评论创建者可以删除
        if request.user.is_superuser or (request.user.is_authenticated and str(request.user.username) == str(db.get_comments_owner('comments',comment_id))):
            db.delete_data('comments', {"_id": ObjectId(comment_id)})
            return JsonResponse({"message": "Comment deleted successfully"}, status=200)
        else:
            return HttpResponseForbidden("You do not have permission to delete this comment.")
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)


@csrf_protect
@login_required
def update_comment_view(request, project_name, comment_id):
    if request.method == "POST":
        from bson import ObjectId
        comment = db.find_data('comments', {"_id": ObjectId(comment_id)})

        if not comment:
            return JsonResponse({"error": "Comment not found"}, status=404)

        # 检查权限：只有评论创建者可以编辑
        if request.user.is_authenticated and str(request.user.id) == str(comment.get("user_id")):
            # 获取新的评论内容
            new_content = request.POST.get("content")
            if not new_content:
                return JsonResponse({"error": "Content cannot be empty"}, status=400)

            db.update_data('comments',[
                {"_id": ObjectId(comment_id)},
                {"$set": {"content": new_content}}]
            )
            return JsonResponse({"message": "Comment updated successfully"}, status=200)
        else:
            return HttpResponseForbidden("You do not have permission to edit this comment.")
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)

#登錄界面
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect('home')
        else:
            return render(request, 'register.html', {'error': 'Username already exists.Please back and log in.'})
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # 登录成功后跳转到首页
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
    return render(request, 'login.html')


def is_admin(user):
    return user.is_superuser  # 只有管理员用户

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(is_admin)
def admin_edit_view(request):
    if request.method == 'POST':
        edit_type = request.POST.get('edit_type')  # 获取编辑类型
        new_content = request.POST.get('content')  # 获取新的内容

        # 验证 edit_type 是否有效
        if edit_type == 'home':
            file_path = os.path.join(MARKDOWN_DIR, 'home.md')
        elif edit_type == 'personal_detail':
            file_path = os.path.join(MARKDOWN_DIR, 'personal_detail.md')
        else:
            return render(request, 'error.html', {'error_message': 'Invalid edit type'})

        # 保存新内容到 Markdown 文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return redirect('home')  # 编辑完成后跳转到首页

    # 读取当前内容
    home_path = os.path.join(MARKDOWN_DIR, 'home.md')
    personal_detail_path = os.path.join(MARKDOWN_DIR, 'personal_detail.md')

    current_home_content = ""
    current_personal_detail_content = ""

    if os.path.exists(home_path):
        with open(home_path, 'r', encoding='utf-8') as f:
            current_home_content = f.read()

    if os.path.exists(personal_detail_path):
        with open(personal_detail_path, 'r', encoding='utf-8') as f:
            current_personal_detail_content = f.read()

    return render(request, 'admin_edit.html', {
        'current_home_content': current_home_content,
        'current_personal_detail_content': current_personal_detail_content,
    })

@login_required
def upload_avatar(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('home')  # 上传成功后跳转主页
    else:
        form = AvatarUploadForm(instance=request.user.profile)
    return render(request, 'upload_avatar.html', {'form': form})

def some_view(request):
    user = request.user
    profile = UserProfile.get_or_create(user)

@login_required
@user_passes_test(is_admin)
def update_contact_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # 更新数据库中的联系方式
        db.update_data('contact', {}, data)
        return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def dashboard_view(request):
    user_name = request.user.username

    # 获取用户最近的评论
    comments = db.find_data("comments", {"name": user_name})
    recent_comments = [
        {"project": comment.get("project_name"), "text": comment.get("text"), "rating": comment.get("rating")}
        for comment in comments
    ]

    # 构造响应数据
    response_data = {
        "recent_comments": recent_comments,
        "username": request.user.username,
        "email": request.user.email,
    }
    return JsonResponse(response_data)

@csrf_exempt
def update_project_view(request, project_id):
    if not request.user.is_authentical or not request.user.is_superuser:
        return JsonResponse({"error":"Unauthorized"},status=403)
    if request.method =='POST':
        try:
            data = json.load(request.body)
            update_name = data.get('name')
            update_description = data.get('description')
            db.update_data(
                'projects',
                {'_id': ObjectId(project_id)},
                {'name':update_name,'description':update_description}
            )
            return JsonResponse({"success":True})
        except Exception as e:
            return JsonResponse({'error':str(e)},status=500)
    return JsonResponse({'error':"Invalid request method"},status=400)