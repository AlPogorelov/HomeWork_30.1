from rest_framework import serializers

from materials.serializers import LessonSerializer
from courses.models import Course
from users.models import Subscription


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'preview', 'description', 'lessons_count', 'lessons', 'is_subscribed']

    def get_lessons_count(self, obj):

        return obj.lessons.count()

    def get_is_subscribed(self, obj):

        user = self.context['request'].user
        if user.is_authenticated:
            return Subscription.objects.filter(user=user, course=obj).exists()
        return False
