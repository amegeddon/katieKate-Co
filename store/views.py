from django.db.models.aggregates import Count
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Product, Collection, OrderItem, Review
from .serialisers import ProductSerializer, CollectionSerializer, ReviewSerializer
from .filters import ProductFilter 

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class =  ProductSerializer
    filter_backends =[DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']

 
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
         if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response ({'error': 'This item cannot be deleted currently as it is associated with an order item'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
         return super().destroy(request, *args, **kwargs)
     
class CollectionViewSet(ModelViewSet) :
    queryset =  queryset =  Collection.objects.annotate(
            products_count=Count('products')).all()
    serializer_class = CollectionSerializer  
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']):
            return Response({'error': 'Collection cannot be deleted at this time because it is associated with one or more products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().destroy(request, *args, **kwargs)
    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    

   
