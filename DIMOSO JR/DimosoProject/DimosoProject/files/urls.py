from django.urls import path
from .import views



urlpatterns = [

   
    path('AploadView/', views.AploadView, name="AploadView"),
    path('<slug:filecourse_slug>/', views.AploadView, name="file_by_category"),
    path('upload_documents', views.upload_documents, name="upload_documents"),
    #path('uploading_task', views.uploading_task, name="uploading_task"),
    path('search_notes', views.search_notes, name="search_notes"),
    path('search_pdf', views.search_pdf, name="search_pdf"),


    #path('base/', views.base, name="base"),
   

    
    
  
  
   
   

 
    
    
 
    
 
]