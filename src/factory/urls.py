from django.conf.urls.defaults import patterns, url

from factory.views import build_lists

urlpatterns = patterns('',
    url(r'^build/create/$', 'factory.views.build_create'),
    url(r'^build/update/(?P<object_id>\d+)/$', 'factory.views.build_update',
     name="build_update"),
    url(r'^build/(?P<object_id>\d+)/$', 'factory.views.build_detail'),
    
    url(r'^build/list/$', build_lists["all"],
        name="build_list_all"),
    url(r'^build/list/success/$', build_lists["success"],
        name="build_list_success"),
    url(r'^build/list/no_success/$', build_lists["no_success"]),
    url(r'^build/list/executed/$', build_lists["executed"]),
    url(r'^build/list/not_executed/$', build_lists["not_executed"]),
    
    # This view is used by the runner
    url(r'^build/oldest_not_executed',
        'factory.views.build_oldest_not_executed',
        name='build_oldest_not_executed')
    
)

