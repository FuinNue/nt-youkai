from django.conf.urls import url, patterns

#from ntyoukai.login import views

urlpatterns = patterns('ntyoukai.login.views',
    url(r'^register/$', 'register'),
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout'),
)
