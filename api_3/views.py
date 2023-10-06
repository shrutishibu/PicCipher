from PIL import Image
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
import pytesseract
import pymongo
import os
from django.conf import settings

class ImageUploadAndList(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [AllowAny]

    def post(self, request):
        uploaded_image = request.FILES.get('image')
       
        if not uploaded_image:
            return Response({"message": "Image not provided"}, status=status.HTTP_400_BAD_REQUEST)

        ocr_text = self.perform_ocr(uploaded_image)
        self.store_data_in_mongodb(uploaded_image, ocr_text)
        return Response({"message": "Image uploaded and processed successfully"}, status=status.HTTP_201_CREATED)

    def perform_ocr(self, image):
        with Image.open(image) as img:
            ocr_text = pytesseract.image_to_string(img)
        return ocr_text
    
    def store_data_in_mongodb(self, uploaded_image, ocr_text):
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        save_path = os.path.join(upload_dir, uploaded_image.name)
        with open(save_path, 'wb') as destination:
            for chunk in uploaded_image.chunks():
                destination.write(chunk)
        image_url = os.path.join(settings.MEDIA_URL, 'uploads', uploaded_image.name)
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["piccipher"]
        image_data_collection = db["imagedata"]
        image_data_collection.insert_one({
            "image_url": image_url,
            "ocr_text": ocr_text,
        })
        client.close()



