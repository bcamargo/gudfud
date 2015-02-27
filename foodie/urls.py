from django.conf.urls import url, patterns
from foodie.views import UserRegistration

urlpatterns = patterns(
    '',
    url(r'users$', UserRegistration.as_view(), name='registration')
)