from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ntyoukai.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^user/', include('ntyoukai.login.urls')),
    url(r'^events/', include('ntyoukai.events.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
