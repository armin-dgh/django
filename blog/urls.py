from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "blog"

urlpatterns = [
    path('', views.index, name="index"),
    path('posts/', views.PostList.as_view(), name="post-list"),
    path('posts/<int:id>', views.post_details, name="post-detail"),
    path('posts/<int:id>/comment/', views.post_comment, name='post-comment'),
    path('ticket/', views.ticket, name="ticket"),
    path('createpost/', views.create_posts, name="create-post"),
    path('createpost/<post_id>', views.edit_post, name="edit-post"),
    path('searchpost/', views.search_posts, name='search-post'),
    path('profile/', views.profile, name='profile'),
    path('post-delete/<post_id>', views.post_delete, name="post-delete"),
    path('image-delete/<img_id>', views.delete_image, name="delete-image"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path('logout/', views.logout_user, name="logout"),




]