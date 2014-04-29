from django.conf.urls import url, patterns

urlpatterns = patterns('ntyoukai.events.views',
    url(r'^$', 'list'),
    url(r'^new/$', 'new'),
    url(r'^event/(?P<event_pk>\d)/$', 'details'),
    url(r'^event/(?P<event_pk>\d)/edit/$', 'edit'),
)
