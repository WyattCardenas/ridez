from rest_framework import serializers
from rides.models import User


class UserSerializer(serializers.ModelSerializer):
    id_user = serializers.IntegerField(help_text='Unique identifier for the user.', read_only=True)
    role = serializers.CharField(help_text='Role of the user in the system.')
    first_name = serializers.CharField(help_text='First name of the user.')
    last_name = serializers.CharField(help_text='Last name of the user.')
    email = serializers.EmailField(help_text='Email address of the user.')
    phone_number = serializers.CharField(help_text='Phone number of the user.')

    class Meta:
        model = User
        fields = ('id_user', 'role', 'first_name', 'last_name', 'email', 'phone_number')
