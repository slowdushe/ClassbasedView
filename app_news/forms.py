from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, EmailMultiAlternatives


class CustomUserForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']


