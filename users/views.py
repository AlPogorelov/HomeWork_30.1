from django.shortcuts import render, get_object_or_404
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from courses.models import Course
from users.models import Payments, User, Subscription
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

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


class SubscriptionAPIView(APIView):

    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():

            subs_item.delete()
            message = 'Подписка удалена'
        else:

            Subscription.objects.create(user=user, course=course_item)
            message = 'Подписка добавлена'

        return Response({"message": message}, status=status.HTTP_200_OK)
