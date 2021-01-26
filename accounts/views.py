from django.shortcuts import render
from rest_framework.decorators import api_view
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def accounts_register_view(request):
    """
    Register a new user
    """
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            token = Token.objects.get(user=account).key
            response_dict = {}
            response_dict["email"] = account.email
            response_dict["token"] = token
            return Response(response_dict, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
