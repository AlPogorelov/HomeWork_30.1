from rest_framework import serializers
from users.models import Subscription
from .models import Lesson
from .validators import MaterialsValidators


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [MaterialsValidators(field='video_url')]


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'
        