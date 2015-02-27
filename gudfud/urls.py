from django.conf.urls import patterns, include, url
import foodie.urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gudfud.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^api/', include(foodie.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
