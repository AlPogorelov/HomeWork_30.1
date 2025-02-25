from django.shortcuts import render
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from users.models import Payments


class PaymentsList(generics.ListAPIView):
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend]
    search_fields = []
    ordering_fields = ['peid_materials', 'payment_method', 'date_pay']
    filterset_fields = ()
