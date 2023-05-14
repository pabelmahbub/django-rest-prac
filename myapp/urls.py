from django.urls import path
from myapp import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    # path('myapi/', views.api_list),
    # path('apidetails/<int:pk>/', views.api_detail),
    
    
    #3.. using class based api view:
    
    #  path('myapi/', views.SnippetList.as_view()),
    #  path('detail/<int:pk>/', views.ApiDetail.as_view()),
    
     #4. generic api view:
     path('gav/', views.ContactList.as_view()),
     path('myDetail/<int:pk>/', views.ContactDetail.as_view()),
     
    
     
     
])