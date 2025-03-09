from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from config.permissions import NotStaff, IsOwnerOrModer
from courses.models import Course
from courses.serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):

    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated & NotStaff | AllowAny]

        elif self.action == 'update' or 'partial_update' or 'destroy' or 'retrieve':
            self.permission_classes = [IsOwnerOrModer]

        return [permission() for permission in self.permission_classes]

    def get_serializer_context(self):

        context = super().get_serializer_context()
        context['request'] = self.request
        return context
