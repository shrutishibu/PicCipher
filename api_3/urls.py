# api_urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('upload-image/', views.ImageUploadAndList.as_view(), name='upload_image'),
    #path('image-data/', views.ImageDataList.as_view(), name='image_data_list'),
]
 