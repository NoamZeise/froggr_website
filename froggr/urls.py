from django.urls import path

from froggr import views

app_name = 'froggr'

urlpatterns = [
    path('',  views.home, name='index'),
    path('home/', views.home, name="home"),
    path('frog-in/', views.frogin, name="frog-in"),
    path('frog-out/', views.frogout, name="frog-out"),
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
    path('profile/<slug:profile_slug>/', views.profile, name="profile"),
    path('create-profile/', views.create_profile, name="create-profile"),
    path('search-results/', views.search_results, name="search-results"),
    path('follow/', views.follow.as_view(), name="follow"),
    path('search-results/<slug:search_query>', views.search_results, name="search-results"),
    path('no-results/', views.no_results, name="no-results"),
    path('create-frogg/', views.create_frogg, name="create-frogg"),
    path('create-frogg/<slug:post_slug>', views.create_frogg, name="create-frogg"),
    path('posts/', views.posts, name='posts'),
    path('posts/<slug:post_slug>/', views.posts, name='posts'),
    path('like-post/', views.like_post, name='like_post'),
    path('following-posts/', views.following_posts, name='following-posts'),
    path('delete/<post_slug>',views.delete_post,name='delete'),
]
