from .models import UploadedFile
from .serializers import UploadedFileCreateSerializer
from rest_framework.generics import CreateAPIView,ListAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
 




class CreateUploadedFileView(CreateAPIView,ListAPIView):
    model = UploadedFile
    serializer_class = UploadedFileCreateSerializer
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
            return UploadedFile.objects.filter(user=self.request.user)

    @swagger_auto_schema()
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.save(user = request.user)
        headers = self.get_success_headers(serializer.data)
        
        url=file.file.url
        url = url.replace("minio","127.0.0.1")
        return Response({"id":file.id,"file_url":url,"type":file.type,"size":file.size}, status=status.HTTP_201_CREATED, headers=headers)
    


class Uploadedlist(ListAPIView):
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        return UploadedFile.objects.filter(user=self.request.user)
    serializer_class = UploadedFileCreateSerializer

class DeleteFile(DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        return UploadedFile.objects.filter(pk = self.kwargs["pk"])
    serializer_class = UploadedFileCreateSerializer




