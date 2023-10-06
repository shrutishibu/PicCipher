# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ImageData
from .serializers import ImageDataSerializer
import pytesseract
import pymongo

class ImageUploadView(APIView):
    def post(self, request):
        uploaded_image = request.FILES['image']
        ocr_text = self.perform_ocr(uploaded_image)
        self.store_data_in_mongodb(uploaded_image, ocr_text)
        return Response({"message": "Image uploaded and processed successfully"}, status=status.HTTP_201_CREATED)

    def perform_ocr(self, image):
        ocr_text = pytesseract.image_to_string(image)
        return ocr_text

    def store_data_in_mongodb(self, uploaded_image, ocr_text):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["piccipher"]
        image_data_collection = db["imagedata"]
        image_data_collection.insert_one({
            "image_url": uploaded_image.url,
            "ocr_text": ocr_text,
        })
        client.close()

class ImageDataList(APIView):
    def get(self, request):
        image_data = ImageData.objects.all()
        serializer = ImageDataSerializer(image_data, many=True)
        return Response(serializer.data)
