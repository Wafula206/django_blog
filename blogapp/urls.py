from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # ✅ One named login
    path('login/', auth_views.LoginView.as_view(template_name='blogapp/login.html'), name='login'),
    # ✅ Optional: second route, no name
    path('accounts/login/', auth_views.LoginView.as_view(template_name='blogapp/login.html')),

    # Your other routes:
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('users/<str:username>/', views.user_profile, name='user_profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]
