from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "blog"

urlpatterns = [
    path('', views.index, name="index"),
    # path('posts/', views.PostList.as_view(), name="post-list"),
    path("posts/", views.post_list, name="post-list"),
    path("posts/<str:category>", views.post_list, name="post-list-category"),
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
    path('passwoed-change/', auth_views.PasswordChangeView.as_view(success_url='done'), name="password_change"),
    path('passwoed-change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='done'), name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/blog/password-reset/complete'), name="password_confirm"),
    path('password-reset/complete', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('register/', views.register, name="register"),
    path("edit-user/", views.edit_user, name="edit-user")


]