from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from api.v1 import views
from django.conf.urls import include

urlpatterns = patterns('',
    url(r'^signup/$', views.UserSignup.as_view()),
    url(r'^me/$', views.UserDetail.as_view()),
    url(r'^me/profile/$', views.ProfileDetail.as_view()),
    url(r'^me/checpoints/$', views.CheckpointsList.as_view()),
    url(r'^me/checpoints/(?P<offset>[0-9]+)/(?P<limit>[0-9]+)/$', views.UserCheckpointsPagination.as_view()),
    url(r'^me/checpoints/(?P<id>[0-9]+)/$', views.NotPlannedCheckpointsList.as_view()),
    url(r'^me/mentors/$', views.MentorList.as_view()),
)

urlpatterns = format_suffix_patterns(urlpatterns)