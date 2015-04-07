from django.conf.urls import url, patterns
from foodie.views import UserRegistration, CustomObtainAuthToken, UserProfile, CurrentMenu, MenuDetail, MenuItemDetail


urlpatterns = patterns(
    '',
    url(r'users$', UserRegistration.as_view(), name='registration'),
    url(r'users/access-token$', CustomObtainAuthToken.as_view(), name='access-token'),
    url(r'users/profile$', UserProfile.as_view(), name='user-profile'),
    url(r'menu', CurrentMenu.as_view(), name='menu-current'),
    url(r'menu/(?P<pk>[0-9]+)', MenuDetail.as_view(), name='menu-detail'),
    url(r'menu/item/(?P<pk>[0-9]+)', MenuItemDetail.as_view(), name='menuitem-detail'),

)