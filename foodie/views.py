from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from foodie.serialiazers import BaseUserSerializer


class UserRegistration(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request, **kwargs):
        serializer = BaseUserSerializer(data=request.DATA)

        if serializer.is_valid():
            base_user = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
