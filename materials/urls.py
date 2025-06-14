from django.urls import path
from .apps import MaterialsConfig
from .views import (LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView,
                    LessonDestroyAPIView)

app_name = MaterialsConfig.name


urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
]
