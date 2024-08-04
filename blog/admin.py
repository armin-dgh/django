from django.contrib import admin
from .models import *
from django_jalali.admin.filters import JDateFieldListFilter


# Register your models here.

# farsi sazi
admin.sites.AdminSite.site_header = "پنل مدیریت جنگو"
admin.sites.AdminSite.site_title = "پنل"
admin.sites.AdminSite.index_title = "پنل مدیریت"

#inlines
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


# 1
# admin.site.register(Post)

# 2
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'status']
    ordering = ['-publish', 'title']
    list_filter = ['status', ('publish', JDateFieldListFilter), 'author']
    search_fields = ['title', 'description']
    raw_id_fields = ['author']  # for foreign key objects
    date_hierarchy = 'publish'
    prepopulated_fields = {'slug': ["title"]}
    list_editable = ["status"]
    list_display_links = ['author', 'title']
    inlines = [CommentInline, ImageInline]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'subject']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "name", "create", "active"]
    list_filter = ["name", "post", "active"]
    list_editable = ["active"]
    search_field = ["name", "massage"]

@admin.register(Image)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["post", "title", "create"]


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["user", 'date_of_birth', "bio", "photo", "job"]