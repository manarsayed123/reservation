from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from tokenize import TokenError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
from authentication.models import User


class CustomLogin(TokenObtainPairView):
    permission_classes = []

    def post(self, request):
        employee_num = request.data.get('employee_num', None)
        print(employee_num)

        password = request.data.get('password', None)
        if password == None:
            raise ValidationError("password field is required")
        if employee_num == None:
            raise ValidationError("employee_num field is required")

        try:
            user = User.objects.get(employee_num=employee_num)
        except:
            raise ValidationError("no registered user")

        serializer = TokenObtainPairSerializer(
            data={'employee_num': user.employee_num, "password": request.data['password']})
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)
