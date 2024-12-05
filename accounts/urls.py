from django.urls import path
from .views import CustomUserCreationView

urlpatterns = [
    path('signup/', CustomUserCreationView.as_view(), name='signup'),

]