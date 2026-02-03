import pandas as pd
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

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

    if 'equipment_type' in df.columns:
        equipment_distribution = df['equipment_type'].value_counts().to_dict()
    else:
        equipment_distribution = {}

    dataset = Dataset.objects.create(
        user=request.user,
        file=file,
        total_count=total_count,
        averages=averages,
        equipment_distribution=equipment_distribution
    )

    # Keep only last 5 datasets
    old_datasets = Dataset.objects.filter(user=request.user).order_by('-uploaded_at')[5:]
    for old in old_datasets:
        old.file.delete()
        old.delete()

    serializer = DatasetSerializer(dataset)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
