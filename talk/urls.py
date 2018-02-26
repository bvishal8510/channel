from django.conf.urls import url
from talk import views
from talk.views import log_in, log_out, user_list, sign_up


urlpatterns = [
    url(r'^log_in/$', views.log_in, name='log_in'),
    url(r'^log_out/$', views.log_out, name='log_out'),
    url(r'^$', views.user_list, name='user_list'),
    url(r'^sign_up/$', sign_up, name='sign_up'),
]