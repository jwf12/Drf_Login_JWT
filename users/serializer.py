from .models import User

from rest_framework import serializers

class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name','email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
