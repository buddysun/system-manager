from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^cmd$',views.commexec),
    url(r'^results/(?P<pk>[0-9]+)/$',views.ret_results),
    url(r'^uploads$',views.uploads_file),
    url(r'^uploads/(?P<pk>[0-9]+)/$',views.send_to_server),
    url(r'^hostlist$',views.host_list),
    url(r'^release$',views.publish),
	url(r'^release/(?P<pk>[0-9]+)/$',views.publish_result),
	url(r'^$',views.release_hist),
	url(r'^rollback$',views.rollback_form),	
	url(r'^backfile_list$',views.backfile_list),
	url(r'^rollback/(?P<pk>[0-9]+)/$',views.rollback_result),		
]
