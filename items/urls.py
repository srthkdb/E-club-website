#this files tells which function/class to call form views.py when the user enters one of the following specified urls
from django.conf.urls import url
from . import views

app_name = 'items' #this app name helps to distinguish eg index.html files of different apps while referencing utls

urlpatterns = [
    # login page
    '''
    homepage showing links to forms to issue items, return issued items, list of location of boxes
    and list of items issued by the given user
    ''',
    #/items/
    url(r'^$', views.index, name='index'),
    #/items/myIssues
    url(r'^myIssues/$', views.myIssues, name='myIssues'),
    #/items/login_user
    url(r'^login_user/$', views.login_user, name='login_user'),
    #/items/logout_user
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    # /home/<box_id>/
    url(r'^(?P<box_id>[0-9]+)/$', views.issues_by_box, name="issues_by_box"),
]

