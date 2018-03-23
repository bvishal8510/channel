from django.conf.urls import url
from talk import views
from django.contrib import admin
from talk.views import log_in, log_out, sign_up, index, create_room, index
# from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', views.index, name='homepage'),
    url(r'^log_in/$', views.log_in, name='log_in'),
    url(r'^log_out/$', views.log_out, name='log_out'),
    # url(r'^$', views.user_list, name='user_list'),
    url(r'^sign_up/$', sign_up, name='sign_up'),
    url(r'^admin/', admin.site.urls),
    url(r'create_room/$', create_room.as_view(), name='create_room'),
    # url(r'^login/$', login, name='login'),  # The base django login view
    # url(r'^logout/$', logout, name='logout'),
]