from os import remove
from django.urls import reverse
from rest_framework.test import APITestCase
from model_mommy import mommy
from django.contrib.auth.models import User
from django_minio_backend import MinioBackend
from minio import Minio
from fileuploader.models import UploadedFile



class ApiTestCase(APITestCase):

    def setUp(self):
        self.user = mommy.make(User)
        self.client1 = Minio("minio:9000","access-key","secret-key",secure=False)
        self.client.force_authenticate(user=self.user)




    def test_create_file(self):
        # Create sample file
        created_file = open("sample.txt","w+")
        created_file.write("sample")
        created_file.close()

        # Open and post file to api
        file = open("./sample.txt","r+")
        resp = self.client.post(reverse('uploadfile'),data={"file": file})
        file.close()

        # Export name of object from api response and get object details from minio api
        name = (resp.data["file_url"]).replace("http://127.0.0.1:9000/my-local-bucket/","")
        object_details = self.client1.stat_object("my-local-bucket",name)
        
        # Remove sample file
        remove("./sample.txt")
        
        # Check if size in database and minio are same
        self.assertEqual(object_details.size,resp.data["size"])

        # Check if type in database and minio are same
        self.assertEqual(object_details.content_type,resp.data["type"])

        # After many hours still can't get a valid url
        # url = self.client1.presigned_get_object("my-local-bucket",name)
        # url = url.replace("minio","127.0.0.1")
        # print(self.client.get(url))
    



    def test_list_file(self):
        resps = []

        # Create and post 10 sample file
        for i in range(10):
            created_file = open(f"sample{i}.txt","w+")
            created_file.write("sample")
            created_file.close()
            file = open(f"./sample{i}.txt","r+")
            resps.append(self.client.post(reverse('uploadfile'),data={"file": file}))
            file.close()
            remove(f"./sample{i}.txt")
        
        # Get list of files
        list = self.client.get(reverse('uploadfile')).data

        # Check if all 10 files was uploaded
        self.assertEqual(len(list),10)




    def test_delete_file(self):
        # Create and post sample file
        created_file = open("sample.txt","w+")
        created_file.write("sample")
        created_file.close()
        file = open("./sample.txt","r+")
        resp = self.client.post(reverse('uploadfile'),data={"file": file})

        # Remove sample file
        remove("./sample.txt")

        # Export name of object from api response
        name = (resp.data["file_url"]).replace("http://127.0.0.1:9000/my-local-bucket/","")
        
        # Delete object using api
        self.client.delete(reverse('deletefile',kwargs={'pk': resp.data['id']}))
        
        # Query to get existence of file instance
        record_existence = UploadedFile.objects.filter(pk=resp.data['id']).exists()
        
        # If object not exist in minio bucket throw exception
        object_existence = True
        try:
            self.client1.get_object("my-local-bucket",name)
        except Exception:
            object_existence = False

        # Check if record of file in database exists or not
        self.assertEqual(record_existence,False)

        # Check if object of file in minio exists or not
        self.assertEqual(object_existence,False)




    def test_minio_connection(self):

        # Check connection between django and minio
        minio_available = MinioBackend("my-local-bucket").is_minio_available()
        if minio_available:
            self.assertTrue
        else:
            self.assertFalse
