from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'nngarage.views.index', name='home'),
    url(r'^signup/$', 'nngarage.views.registration', name='registration'),

    # TODO: do the login template page
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'nngarage/login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login', name='logout'),

    url(r'control-panel/$', 'nngarage.views.index', name='control_panel'),
    # url(r'get-nn-desc/(?P<username>[A-Za-z]\w*)/$', 'nngarage.views.get_nn_desc', name='get_nn_desc'),
    # url(r'upload-nn-desc/$', 'nngarage.views.add_nn_desc', name='add_nn_desc'),

    # TODO: password rest page

    # TODO: task related link
    url(r'add-task', 'nngarage.views.add_task', name='add_task'),

    url(r'exp-download/$', 'nngarage.views.exp_download', name='exp_download'),
    url(r'files/$', 'nngarage.views.files'),
    url(r'get-tasks', 'nngarage.views.get_tasks', name='get_tasks'),
    url(r'get-task-update', 'nngarage.views.get_task_update', name='get_task_update'),
]
