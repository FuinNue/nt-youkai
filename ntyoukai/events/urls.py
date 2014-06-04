from django.conf.urls import url, patterns

urlpatterns = patterns('ntyoukai.events.views',
    url(r'^$', 'list'),
    url(r'^new/$', 'new'),
    url(r'^event/(?P<event_pk>\d)/$', 'details'),
    url(r'^event/(?P<event_pk>\d)/(?P<invite_pk>\d)/$', 'details_invited'),
    url(r'^event/(?P<event_pk>\d)/edit/$', 'edit'),
    url(r'^event/(?P<event_pk>\d)/invite/$', 'invite'),
    url(r'^event/(?P<event_pk>\d)/post-entry/$', 'post_entry'),
    url(r'^event/(?P<event_pk>\d)/attend/(?P<invite_pk>\d)/$', 'accept_invite'),
    url(r'^event/(?P<event_pk>\d)/reject/(?P<invite_pk>\d)/$', 'reject_invite'),
    url(r'^event/(?P<event_pk>\d)/leave/$', 'leave'),
    url(r'^event/(?P<event_pk>\d)/remove/(?P<user_pk>\d)/$', 'remove_user'),
)
