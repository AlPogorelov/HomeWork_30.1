from rest_framework import serializers

from materials.serializers import LessonSerializer
from courses.models import Course


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'course_name', 'preview', 'description', 'lessons_count', 'lessons']

    def get_lessons_count(self, obj):

        return obj.lessons.count()
