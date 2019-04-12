from django.contrib import admin
from django.urls import *
from missionapp import views
from django.conf.urls import *
from django.contrib.auth.views import (
     PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView,
)

urlpatterns=[
path('user/',views.userposts,name='user_posts'),
url(r'^tinymce/', include('tinymce.urls')),
url(r'^profile/password/$',PasswordChangeView.as_view(success_url=reverse_lazy('password_change_done')), name='change_password'),
path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),

url(r'^reset-password/$', PasswordResetView.as_view(), {'template_name': 'missionapp/reset_password.html', 'post_reset_redirect': 'password_reset_done', 'email_template_name': 'final_app/reset_password_email.html'}, name='reset_password'),

url(r'^reset-password/done/$',PasswordResetDoneView.as_view() , {'template_name': 'missionapp/reset_password_done.html'}, name='password_reset_done'),

url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',PasswordResetConfirmView.as_view() , {'template_name': 'missionapp/reset_password_confirm.html', 'post_reset_redirect': 'password_reset_complete'}, name='password_reset_confirm'),

url(r'^reset-password/complete/$', PasswordResetCompleteView.as_view(),{'template_name': 'missionapp/reset_password_complete.html'}, name='password_reset_complete'),

url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
url(r'^profile/$', views.view_profile, name='view_profile'),
#path('s/',views.multipleView,name='multiple_view'),
#patterns('',(r'^cat/(?P<pk>\d+)/$',views.PostCreateView.as_view(),name='post_new'),(r'^cat/(?P<pk>\d+)/$',views.PostCategory.as_view(),name='post_by_category'),),
path('catlist/',views.categoryList,name='category_list'),
#path('cat/x/',views.categoryList,name='category_list'),
url(r'^cat/(?P<pk>\d+)/$',views.PostCategory,name='post_by_category'),
path('',views.IndexView.as_view(),name='index'),
#url(r'^category/(?P<hierarchy>.+)/$', views.show_category, name='category'),
path('register/',views.register,name='register'),
path('login/',views.user_login,name='user_login'),
#path('',views.PostListView.as_view(),name='post_list'),
path('post/',views.post_list,name='post_list'),
path('about/',views.AboutView.as_view(),name='about'),
url(r'^post/(?P<pk>\d+)/$',views.PostDetailView.as_view(),name='post_detail'),
url(r'^post/new/$',views.PostCreateView,name='post_new'),
#path('cat/(?P<pk>\d+)/',views.PostCreateView.as_view(),name='post_new'),
url(r'^post/(?P<pk>\d+)/edit/$',views.PostUpdateView,name='post_edit'),
url(r'^post/(?P<pk>\d+)/remove/$',views.PostDeleteView.as_view(),name='post_remove'),
path('drafts/',views.DraftListView.as_view(),name='post_draft_list'),
url(r'^post/(?P<pk>\d+)/publish/$',views.post_publish,name='post_publish'),
url(r'^post/(?P<pk>\d+)/comment/$',views.add_comment_to_post,name='add_comment_to_post'),
url(r'^comment/(?P<pk>\d+)/approve/$',views.comment_approve,name='comment_approve'),
url(r'^comment/(?P<pk>\d+)/remove/$',views.comment_remove,name='comment_remove'),
path('privacy_policy/',views.privacy_policy.as_view(),name='privacy_policy'),
path('termsandcondition/',views.termsandcondition.as_view(),name='termsandcondition'),
path('contactus/',views.contactus.as_view(),name='contactus'),
path('pressrelease/',views.pressrelease.as_view(),name='pressrelease'),

]
