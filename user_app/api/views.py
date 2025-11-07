from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user_app.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from user_app import models     # We are importing entire models file, because generation of token happens in that file.

@api_view(["POST"])
def registration_view(request):
    
    if request.method == "POST":
        serializer = RegistrationSerializer(data = request.data)
        
        # Creating an empty dictionary 
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data["username"] = account.username
            data["email"] = account.email            
            
            token = Token.objects.get(user = account).key
            
            data["token"] = token
            
            return Response(data, status = status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def logout_view(request):
    
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status = status.HTTP_200_OK)
