from django.urls import path, include

from .views import CreateUploadedFileView, DeleteFile, Uploadedlist


urlpatterns = [
    path('upload/', CreateUploadedFileView.as_view(), name='uploadfile'),
    path('upload/<int:pk>/', DeleteFile.as_view(), name='deletefile')
]