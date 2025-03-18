from django.urls import path
from .views import MyTokenObtainPairView, UsersViewSet, SubscriptionAPIView, PaymentsCreateAPIView
from .apps import UsersConfig
from rest_framework.routers import DefaultRouter

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'users', UsersViewSet, basename='users')


urlpatterns = [
    path('payment', PaymentsCreateAPIView.as_view(), name='payment'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('subscription/', SubscriptionAPIView.as_view(), name='subscribe'),
] + router.urls
