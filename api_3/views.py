from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import ImageData
from .serializers import ImageDataSerializer
import pytesseract
import pymongo

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

    def get(self, request):
        image_data = ImageData.objects.all()
        serializer = ImageDataSerializer(image_data, many=True)
        return Response(serializer.data)
