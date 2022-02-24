from django.urls import path
from .import views



urlpatterns = [

   
    path('chat-home/', views.home, name="chat-home"),
    
    path('base/', views.base, name="base"),
    path('send/', views.send_chat, name='chat-send'),
    path('renew/', views.get_messages, name='chat-renew'),
    
  
  
   
   

 
    
    
 
    
 
]