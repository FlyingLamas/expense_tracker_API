from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}
        # extra_kwargs is a pre defined keyword recognized by DRF.
        # Purpose - It lets you specify extra field level settings without redefining the fields explicitly.
        # write only - true, instructs DRF that this field can be written into during post or put, but can never be included in responses.
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user