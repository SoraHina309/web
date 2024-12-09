"""
URL configuration for new project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from django.contrib import admin
from myapp import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns =[
    path('',views.home,name='home'),
    path('api/home/', views.api_home_markdown, name='api_home'),
    path('api/personal_detail/', views.api_personal_detail_markdown, name='api_personal_detail'),
    path('api/hobbies/', views.api_hobbies_markdown, name='api_hobbies'),  # Skills 数据 API
    path('api/personal_experience/', views.api_personal_experience, name='api_personal_experience'),  # Projects 数据 API
    path('api/contact/', views.api_contact, name='api_contact'),  # Contact 数据 API
    path('personal_detail/', views.personal_detail, name='personal_detail'),
    path('api/dashboard/',views.dashboard_view, name='dashboard'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_edit/', views.admin_edit_view, name='admin_edit'),

    path('api/user_status/', views.user_status_view, name='user_status'),

    # path('api/projects/', views.project_list_view, name='project_list'),
    # path('api/projects/<str:project_name>/', views.project_detail_view, name='project_detail'),
    # path('api/projects/<str:project_name>/rate/', views.project_rate_view, name='project_rate'),
    # path('api/projects/<str:project_name>/comment/', views.project_comment_view, name='project_comment'),


    # path('api/personal_experience/', views.personal_experience_list_view, name='personal_experience_list'),
    # path('api/personal_experience/<str:project_name>/', views.personal_experience_detail_view, name='personal_experience_detail'),

    path('api/comments/<str:project_name>/', views.get_comments_view, name='get_comments'),
    path('api/comments/<str:project_name>/submit/', views.submit_comment_view, name='submit_comment'),
    path('api/comments/<str:project_name>/update/<str:comment_id>/', views.update_comment_view, name='update_comment'),
    path('api/comments/<str:project_name>/delete/<str:comment_id>/', views.delete_comment_view, name='delete_comment'),
    path('upload_avatar/', views.upload_avatar, name='upload_avatar'),
    path("api/update_contact/", views.update_contact_view, name="update_contact"),
    path('api/update_project/<str:project_name>',views.update_project_view,name="update_project"),

    

    # path('',views.home,name='home'),
    # path('api/projects/',views.api_projects,name='api_projects'),
    # path('api/skills/',views.api_skills,name='api_skills'),
    # path('api/contact/',views.api_contact,name='api_contact'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

