from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('', views.index, name="index"),
    path('posts/', views.PostList.as_view(), name="post-list"),
    path('posts/<int:id>', views.post_details, name="post-detail"),
    path('posts/<int:id>/comment/', views.post_comment, name='post-comment'),
    path('ticket/', views.ticket, name="ticket"),
    path('createpost/', views.create_posts, name="create-post"),
    path('createpost/<post_id>', views.edit_posts, name="edit-post"),
    path('searchpost/', views.search_posts, name='search-post'),
    path('profile/', views.profile, name='profile'),
    path('post-delete/<post_id>', views.post_delete, name="post-delete"),

]