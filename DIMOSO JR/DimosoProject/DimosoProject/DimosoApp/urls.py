from django.urls import path
from .import views



urlpatterns = [

   
    path('home/', views.home, name="home"),
    path('base/', views.base, name="base"),
    path('uchafu/', views.uchafu, name="uchafu"),
    
    path('<slug:category_slug>/', views.home, name="post_by_category"),
    

    path('search_post', views.search_post, name="search_post"),
    path('PostDetail/<str:pk>', views.PostDetail.as_view(), name="PostDetail"),
    path('post_comments', views.post_comments, name="post_comments"),
    path('blog_users', views.blog_users, name="blog_users"),

    path('update_blog_user/<str:pk>', views.update_blog_user.as_view(), name="update_blog_user"),
    path('delete_blog_user/<int:pk>/', views.delete_blog_user, name="delete_blog_user"),

    path('send_email_to_dimoso', views.send_email_to_dimoso, name="send_email_to_dimoso"),



    
    
  
  
   
   

 
    
    
 
    
 
]