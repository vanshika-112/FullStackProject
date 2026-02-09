import os
import pandas as pd
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from django.conf import settings

from .models import Dataset
from .serializers import DatasetSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def test_api(request):
    return Response({"message" : "API is working"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    file = request.FILES.get('file')

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    df = pd.read_csv(file)

    total_count = len(df)

    averages = df.mean(numeric_only=True).to_dict()

    if 'Type' in df.columns:
        equipment_distribution = df['Type'].value_counts().to_dict()
    else:
        equipment_distribution = {}

    dataset = Dataset.objects.create(
        user=request.user,
        file=file,
        total_count=total_count,
        averages=averages,
        equipment_distribution=equipment_distribution
    )

    # -------- PDF GENERATION (ADDED) --------
    pdf_dir = os.path.join(settings.MEDIA_ROOT, "reports")
    os.makedirs(pdf_dir, exist_ok=True)

    pdf_path = os.path.join(pdf_dir, "report.pdf")

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "CSV Analysis Report")

    y -= 40
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Total Records: {total_count}")

    y -= 30
    c.drawString(50, y, "Averages:")
    y -= 20

    for key, value in averages.items():
        c.drawString(70, y, f"{key}: {value}")
        y -= 20

    y -= 20
    c.drawString(50, y, "Equipment Distribution:")
    y -= 20

    for key, value in equipment_distribution.items():
        c.drawString(70, y, f"{key}: {value}")
        y -= 20

    c.showPage()
    c.save()

    pdf_url = request.build_absolute_uri(
        settings.MEDIA_URL + "reports/report.pdf"
    )

    # Keep only last 5 datasets
    old_datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')[5:]
    for old in old_datasets:
        old.file.delete()
        old.delete()

    serializer = DatasetSerializer(dataset)

    response_data = serializer.data
    response_data["pdf_url"] = pdf_url

    return Response(response_data, status=status.HTTP_201_CREATED)

class LastFiveDatasetsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        datasets = Dataset.objects.filter(
            user=request.user
        ).order_by('-uploaded_at')[:5]

        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)