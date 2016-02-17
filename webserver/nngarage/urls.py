from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'nngarage.views.index', name='home'),
    url(r'^signup/$', 'nngarage.views.registration', name='registration'),

    # TODO: do the login template page
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'nngarage/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    url(r'control-panel/$', 'nngarage.views.index', name='control_panel'),
    url(r'get-nn-desc/(?P<username>[A-Za-z]\w*)/$', 'nngarage.views.get_nn_desc', name='get_nn_desc'),
    url(r'upload-nn-desc/$', 'nngarage.views.add_nn_desc', name='add_nn_desc'),
    # TODO: password rest page
]
