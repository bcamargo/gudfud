from django.conf.urls import url, patterns
from foodie.views import UserRegistration, CustomObtainAuthToken, TestView


urlpatterns = patterns(
    '',
    url(r'users$', UserRegistration.as_view(), name='registration'),
    url(r'users/access-token$', CustomObtainAuthToken.as_view(), name='access-token'),
    url(r'test', TestView.as_view(), name='test')
)