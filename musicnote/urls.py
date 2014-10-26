from django.conf.urls import patterns, include, url

from django.contrib import admin
from mn.views import *
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'musicnote.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index,name='index'),
    url(r'^nodes/$', nodes,name='nodes'),
    url(r'^users/$', users,name='users'),
    url(r'^signin/$', signin,name='signin'),
    url(r'^signout/$', signout,name='signout'),
    url(r'^setting/$',setting,name='setting'),
    url(r'^register/$',register,name='register'),
    url(r'^setting/avatar/$',avatar,name='avatar'),
    url(r'^gravatar/$',gravatar,name='gravatar'),
    url(r'^node/(.*)$',nodetopics,name='nodetopics'),

    url(r'^f/node/(.*)$',follownode,name='follownode'),
    url(r'^f/topic/(.*)$',followtopic,name='followtopic'),
    url(r'^f/user/(.*)$',followuser,name='followuser'),

    url(r'^t/create/(.*)$',createtopic,name='createtopic'),
    url(r'^t/edit/(\d+)$',edittopic,name='edittopic'),
    url(r"^t/(\d+)$", topicview,name='topicview'),
    url(r"^member/(.*)$", member_info,name='member_info'),
    url(r'^m/(.*)/$',createmessage,name='createmessage'),
    url(r'^u/(.*)/topics/$',user_topics,name='user_topics'),
    url(r'^u/(.*)/replies/$',user_replies,name='user_replies'),
    url(r'^u/(.*)/collections/$',user_collections,name='user_collections'),
    



)
