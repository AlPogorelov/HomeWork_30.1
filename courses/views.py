from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from config.permissions import NotStaff, IsOwnerOrModer
from courses.models import Course
from courses.serializers import CourseSerializer
from users.tasks import send_course_update_email


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

    def perform_update(self, serializer):
        instance = serializer.save()
        # Запускаем асинхронную задачу
        send_course_update_email.delay(instance.id)
