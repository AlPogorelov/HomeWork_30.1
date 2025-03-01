from django.urls import path
from .views import MyTokenObtainPairView, UsersViewSet
from .apps import UsersConfig
from rest_framework.routers import DefaultRouter

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')


urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
] + router.urls
