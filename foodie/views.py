from rest_framework import status, parsers, renderers
from rest_framework.authentication import get_authorization_header
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
# from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from social.apps.django_app.utils import strategy, psa
from foodie.serialiazers import BaseUserSerializer
from rest_framework.authtoken import views as authtoken_views


class CustomObtainAuthToken(authtoken_views.ObtainAuthToken):
    def post(self, request):

        backend = request.DATA.get('backend')
        backend = 'google-oauth2' if backend == 'google' else backend

        if backend == 'auth':
            return super(CustomObtainAuthToken, self).post(request)
        else:
            # Here we call PSA to authenticate like we would if we used PSA on server side.

            user = register_by_access_token(request, backend)

            # If user is active we get or create the REST token and send it back with user data
            if user and user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'id': user.id, 'email': user.email, 'token': token.key})


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


@psa()
def register_by_access_token(request, backend):
    backend = request.backend
    # Split by spaces and get the array

    access_token = request.DATA.get('token')
    # Real authentication takes place here
    user = backend.do_auth(access_token)

    return user


class TestView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)