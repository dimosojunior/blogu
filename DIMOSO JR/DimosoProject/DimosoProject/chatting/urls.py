from django.urls import path
from .import views



urlpatterns = [

   
   # path('chatroom/', views.chatroom, name="chatroom"),
    path("<int:pk>/", views.chatroom, name="chatroom"),
    path("ajax/<int:pk>/", views.ajax_load_messages, name="chatroom-ajax"),
        
   

    
    
  
  
   
   

 
    
    
 
    
 
]