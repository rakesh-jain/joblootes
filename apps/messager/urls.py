from django.urls import path
from .views import EmailAPIView


urlpatterns = [
    path('send-email/', EmailAPIView.as_view(),name='send-email'),
]