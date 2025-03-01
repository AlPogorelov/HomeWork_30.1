from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from users.models import Payments, User
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets

from users.serializers import MyTokenObtainPairSerializer, UserSerializer


class PaymentsList(generics.ListAPIView):
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend]
    search_fields = []
    ordering_fields = ['peid_materials', 'payment_method', 'date_pay']
    filterset_fields = ['peid_materials', 'payment_method', 'date_pay']


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UsersViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    queryset = User.objects.all()
