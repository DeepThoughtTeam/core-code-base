from django.conf.urls import url

urlpatterns = [
    # url(r'^uidemo/', include('user_interface_demo.urls')),
    url(r'^$', 'ui_service.views.index', name='index'),
]