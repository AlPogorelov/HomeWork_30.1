from django.shortcuts import render
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from config.permissions import NotStaff, IsOwner
from courses.models import Course
from courses.serializers import CourseSerializer


class IsAuthenticated:
    pass


class CourseViewSet(viewsets.ViewSet):

    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated & NotStaff]

        elif self.action == 'update' or 'partial_update' or 'destroy':
            self.permission_classes = [IsOwner]

        return [permission() for permission in self.permission_classes]
