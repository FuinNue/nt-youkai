from django.conf.urls import url, patterns

urlpatterns = patterns('ntyoukai.main.views',
    url(r'^$', 'home'),
)
