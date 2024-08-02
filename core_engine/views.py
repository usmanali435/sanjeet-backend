import os
import random
import datetime
import cv2
import supervision as sv
from PIL import Image
import matplotlib.pyplot as plt
from roboflow import Roboflow
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class EngineView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def save_uploaded_file(self, file):
        """
        Save the uploaded file to the specified path.
        """
        upload_dir = os.path.join(settings.MEDIA_ROOT, "temp")
        os.makedirs(upload_dir, exist_ok=True)  # Ensure the directory exists
        upload_path = os.path.join(upload_dir, file.name)
        
        try:
            with open(upload_path, "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return upload_path
        except Exception as e:
            print(f"Error saving file: {e}")
            raise

    def process_image(self, image_path):
        """
        Process the image using the Roboflow model and return the annotated image path.
        """
        rf = Roboflow(api_key=settings.ROBO_API_KEY)
        project = rf.workspace().project("stage-1-launch")
        model = project.version(1).model
        prediction = model.predict(image_path, confidence=1).json()

        # Process and save annotated image
        labels = [item["class"] for item in prediction["predictions"]]
        detections = sv.Detections.from_roboflow(prediction)
        label_annotator = sv.LabelAnnotator()
        mask_annotator = sv.MaskAnnotator()
        image = cv2.imread(image_path)
        annotated_image = mask_annotator.annotate(scene=image, detections=detections)
        annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections, labels=labels)
        sv.plot_image(image=annotated_image, size=(16, 16))
        
        # Convert the NumPy array to a PIL image
        annotated_image_pil = Image.fromarray(annotated_image)
        plt.ioff()

        # Generate a random filename for the analyzed image
        current_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_number = random.randint(1000, 9999)
        random_filename = f"{current_datetime}-{random_number}.jpeg"

        # Define the URL for the saved image
        analyzed_image_url = f"/media/analyzed/{random_filename}"  # Update the path as needed
        output_image_path = os.path.join(settings.MEDIA_ROOT, "analyzed", random_filename)

        # Ensure the analyzed directory exists
        os.makedirs(os.path.dirname(output_image_path), exist_ok=True)

        # Save the annotated image to the output path
        annotated_image_pil.save(output_image_path)

        return analyzed_image_url, output_image_path

    def post(self, request):
        try:
            image_path = request.FILES.get("file")
            
            try:
                user = User.objects.get(email=request.user.email)
            except User.DoesNotExist:
                return Response({"success": False, "message": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

            if not image_path or not user.email:
                return Response({"error": "File and email are required."}, status=status.HTTP_400_BAD_REQUEST)

            # Save uploaded file
            upload_path = self.save_uploaded_file(image_path)
            
            # Process the image and get the annotated image URL
            analyzed_image_url, output_image_path = self.process_image(upload_path)
            
            content = {
                "url": analyzed_image_url,
            }

            return Response(content, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
