from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
   
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('logout/', views.logout_view, name='logout'),
    
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
   
    


]
