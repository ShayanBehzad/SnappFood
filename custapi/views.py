from collections import OrderedDict
import json
import re
from urllib import request
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import *
from .forms import *
from register.models import User
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action





# class CustomerListCreateView(generics.ListCreateAPIView):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer



class CustomerListCreateView(viewsets.ModelViewSet):

    
    def get_queryset(self):
        return Customer.objects.all()

    # serializer_class = CustomerSerializer
    action_serializer = {
        'list': CustomerSerializer,
        'create': CustomerCreateSerializer
    }

    def get_serializer_class(self):
        if self.action == 'list':
            return CustomerSerializer
        elif self.action == 'create':
            return CustomerCreateSerializer
        return None
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        re_da = request.data
        print(request.data)
        serializer = serializer_class(data={
            'username':re_da['username'],
            'email':re_da['email'],
            'phone':re_da['phone'],
            'password':re_da['password'],
        })
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer




class AddressView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AddressSerializer

    def get_queryset(self):
        custom = get_object_or_404(Customer, user=self.request.user)
        print(custom)
        return Address.objects.filter(cust=custom)


    def update(self, request, *args, **kwargs):
        # custom = get_object_or_404(Customer, user=self.request.user)
        instanse = self.get_object()
        serializer = self.get_serializer(instanse, request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_update(serializer)
        except ValidationError as e:
            return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"msg":"Current address updated successfully"}, status=status.HTTP_200_OK)  
    
    def create(self, request, *args, **kwargs):
        serializer = AddressSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            self.perform_create(serializer)
        return Response({"msg": "Address added successfully."}, status=status.HTTP_201_CREATED)



class RestaurantSpView(viewsets.ViewSet):
    queryset = Restaurant.objects.all()
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = Restaurant.objects.all()
        serializer = RestaurantsListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = Restaurant.objects.all()
        restaurant = get_object_or_404(queryset, id=pk)
        serializer = RestaurantSerializer(restaurant)
        return Response(serializer.data)


class FoodsView(viewsets.ViewSet):

    # get the foods belonging to the chosen restaurant:
    def get_queryset(self):
        # restaurant_id = self.request.query_params.get('pk', None)
        restaurant_id = self.kwargs['pk']
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        # Filter FoodCategory instances that have Food instances related to the restaurant
        queryset = FoodCategory.objects.filter(category_foods__in=restaurant.foods.all())
        return queryset

    def list(self, request, pk=None):
        serializer = CategorySerializer(self.get_queryset(), many=True)
        return Response(serializer.data)
    

class CartView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ItemSerializer


    def get_queryset(self):
        customer = Customer.objects.get(user_id=self.request.user.id)
        # get_object_or_404(Customer, user=self.request.user)
        # cart = get_object_or_404(Cart, customer=customer)
        cart = Cart.objects.filter(customer=customer)
        return cart

    def list(self, request):
        queryset = self.get_queryset()
        serializer = CartSerializer(queryset, many=True)
        serializer_data = serializer.data
        # serializer_data['foods'] = CartItem.objects.get()
        return Response(serializer_data)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Cart, id=pk)
        serializer = CartSerializer(queryset)
        return Response(serializer.data)
    
    def add(self, request, pk=None):
        # if exists, update it else create one
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(cart_id=pk)
            cart_id = pk
            print(serializer.data)

            return Response({'msg': 'sucssesfully added', 'cart_id': cart_id})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def pay(self, request, pk=None):
    #     # if valid, add to orders
    #     queryset = get_object_or_404(Cart, id=pk)
    #     serializer = CartSerializer(queryset)
    #     if serializer.is_valid():
    #         Order.objects.create(customer=request.user, restaurant=serializer.data['restaurant'],
    #                               state=1, content=serializer.data['foods'][:3], amount_paid=serializer.data['food']['price'])
    #         queryset.delete()
    #         return Response({"msg":'payment succseed'})
    #     return Response(serializer.errors)
    


class CartCreateView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartCreateSerializer
    def create(self, request):
        serializer_cl = self.serializer_class
        serializer = serializer_cl(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)



class Payment(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    # serializer_class = PaymentSerializer
    
    def pay(self, request, pk=None):
        # if valid, add to orders
        queryset = get_object_or_404(Cart, id=pk)
        serializer = CartSerializer(queryset)
        # if serializer.is_valid():
        amount_paid = 0
        for i in serializer.data['foods']:
            amount_paid += i['price']
        print(serializer.data['foods'])
        jsonstr = json.dumps(serializer.data['foods'], indent=4, default=str)
        order_serializer = OrderSerializer(data={
            'cus': Customer.objects.get(user_id=request.user.id).subscription,
            'restaurant': serializer.data['restaurant']['id'],
            'state': 1,
            'content':jsonstr,
            'amount_paid':amount_paid,
        })
        if order_serializer.is_valid():
            order_serializer.save()
            queryset.delete()
            return Response({"msg":'payment succseed'})
            # Order.objects.create(customer=request.user, restaurant=serializer.data['restaurant'],
            # state=1, content=serializer.data['foods'][:3], amount_paid=serializer.data['food']['price'])
            
        return Response(order_serializer.errors)
    

    # def get_objects(self, pk):
    #     return CartItem.objects.get(id=pk)
    

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_objects(pk=kwargs.get('id'))
    #     serializer = ItemSerializer(instance, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save
    #         return Response({'msg': 'sucssesfully added', 'status': status.HTTP_200_OK})
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class CommentView(viewsets.ViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = CommentSerializer

#     def get_queryset(self, pk=None):
#         com = Comment.objects.filter(restaurant_id=pk)
#         return com

#     def list(self, request, pk=None):
#         queryset = self.get_queryset(pk=pk)
#         serializer = self.serializer_class(queryset, many=True)

#         return Response(serializer.data)

    # def add(self, request, pk=None):
    #     # queryset = self.get_queryset(pk=pk)
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"msg": "comment created successfully"})
        
    #     return Response(serializer.data)
    
class CommentView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    action_serializers = {
        'create': CommentCreateSerializer,
        'list': CommentSerializer,
    }
    
    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)
        return super().get_serializer_class()
    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return CommentSerializer
    #     else:
    #         return None
    

    def get_queryset(self, pk=None):
        com = Comment.objects.filter(restaurant_id=pk)
        return com

    def list(self, request, pk=None):
        queryset = self.get_queryset(pk=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        return Response(serializer.data)
    
    def get_serializer_context(self, pk=None):
        context = super().get_serializer_context()
        context['pk'] = pk
        return context
    
    def create(self, request, pk=None):
        serializer_class = self.get_serializer_class()

        req_data = request.data
        # req_data['restaurant_id'] = pk
        serializer = serializer_class(data=req_data, context={'request': request, 'pk':pk})
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "comment created successfully"})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
