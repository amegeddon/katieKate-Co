from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serialisers import ProductSerializer, CollectionSerializer

# Create your views here.
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Corrected: Added parentheses to execute the save
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET', 'PUT'])
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id) 
    if request.method == 'GET':
        serializer = ProductSerializer(product, context={'request': request})  
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data, context={'request': request}) 
        serializer.is_valid(raise_exception=True)
        serializer.save()  
        return Response(serializer.data, status=status.HTTP_200_OK)  

@api_view(['GET'])
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk) 
    serializer = CollectionSerializer(collection, context={'request': request}) 
    return Response(serializer.data)
    
    
    