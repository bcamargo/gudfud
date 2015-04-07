from rest_framework import status, parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken import views as authtoken_views
from social.apps.django_app.utils import psa
from foodie.models import Customer, Menu, MenuItem
from foodie.serialiazers import BaseUserSerializer, CustomerSerializer, OperatorSerializer, MenuSerializer, \
    MenuItemSerializer
from rest_framework import generics


class CustomObtainAuthToken(authtoken_views.ObtainAuthToken):
    def post(self, request):

        backend = request.DATA.get('backend')

        if backend:
            backend = 'google-oauth2' if backend == 'google' else backend

            if backend == 'auth':
                return super(CustomObtainAuthToken, self).post(request)
            else:
                # Here we call PSA to authenticate like we would if we used PSA on server side.

                user = register_by_access_token(request, backend)

                if user.get_named_user() is None:
                    # Create customer
                    Customer.objects.create(base_user=user)

                # If user is active we get or create the REST token and send it back with user data
                if user and user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'id': user.id, 'email': user.email, 'token': token.key})
        else:
            return Response(data={'backend': ['This field is required']},
                            status=status.HTTP_400_BAD_REQUEST)


class UserRegistration(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, **kwargs):
        serializer = BaseUserSerializer(data=request.DATA)

        if serializer.is_valid():
            base_user = serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    def get(self, request, **kwargs):
        named_user = request.user.get_named_user()

        if named_user:
            if named_user.is_customer:
                serializer_class = CustomerSerializer
            else:
                serializer_class = OperatorSerializer

            serializer = serializer_class(instance=named_user, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': 'User without customer nor operator'})

    def patch(self, request, **kwargs):
        named_user = request.user.get_named_user()
        data = request.DATA

        if named_user:
            if named_user.is_customer:
                serializer_class = CustomerSerializer
            else:
                serializer_class = OperatorSerializer

            serializer = serializer_class(instance=named_user, data=data, context={'request': request})

            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentMenu(APIView):
    def get(self, request, **kwargs):
        menu = Menu.objects.get_current_menu()
        serializer = MenuSerializer(instance=menu, context={'request': request})
        return Response(data=serializer.data)


class MenuDetail(generics.RetrieveAPIView):
    model = Menu
    serializer_class = MenuSerializer


class MenuItemDetail(generics.RetrieveAPIView):
    model = MenuItem
    serializer_class = MenuItemSerializer

@psa()
def register_by_access_token(request, backend):
    backend = request.backend
    # Split by spaces and get the array

    access_token = request.DATA.get('token')
    # Real authentication takes place here
    user = backend.do_auth(access_token)

    return user

