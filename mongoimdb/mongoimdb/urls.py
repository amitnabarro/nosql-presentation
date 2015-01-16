from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'simple_insert/','movies.views.simple_insert'),
    
    url(r'simple_insert_handler/','movies.views.simple_insert_handler'),

	url(r'group_by/$','movies.views.group_by'),
    
)
