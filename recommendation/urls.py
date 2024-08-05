# recommendation/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='recommendation/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='recommendation/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='recommendation/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='recommendation/password_reset_complete.html'), name='password_reset_complete'),
    path('crops/', views.crop_list, name='crop_list'),
    path('crop/create/', views.crop_create, name='crop_create'),
    path('crop/update/<int:pk>/', views.crop_update, name='crop_update'),
    path('crop/delete/<int:pk>/', views.crop_delete, name='crop_delete'),
    path('knowledge/', views.knowledge_list, name='knowledge_list'),
    path('knowledge/create/', views.knowledge_create, name='knowledge_create'),
    path('knowledge/update/<int:pk>/', views.knowledge_update, name='knowledge_update'),
    path('knowledge/delete/<int:pk>/', views.knowledge_delete, name='knowledge_delete'),
    path('knowledge_rule/', views.knowledge_rule_list, name='knowledge_rule_list'),
    path('knowledge_rule/create/', views.knowledge_rule_create, name='knowledge_rule_create'),
    path('knowledge_rule/update/<int:pk>/', views.knowledge_rule_update, name='knowledge_rule_update'),
    path('knowledge_rule/delete/<int:pk>/', views.knowledge_rule_delete, name='knowledge_rule_delete'),
    path('knowledge_fuzzy_value/', views.knowledge_fuzzy_value_list, name='knowledge_fuzzy_value_list'),
    path('knowledge_fuzzy_value/create/', views.knowledge_fuzzy_value_create, name='knowledge_fuzzy_value_create'),
    path('knowledge_fuzzy_value/update/<int:pk>/', views.knowledge_fuzzy_value_update, name='knowledge_fuzzy_value_update'),
    path('knowledge_fuzzy_value/delete/<int:pk>/', views.knowledge_fuzzy_value_delete, name='knowledge_fuzzy_value_delete'),
    path('recommend_crop/', views.crop_recommendation, name='crop_recommendation'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
