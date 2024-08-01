from django import template
from django.contrib.auth.models import User
from ..models import Post, Comment
from django.db.models import Count, Max
from markdown import markdown
from django.utils.safestring import mark_safe
# from sansorchi import Sansorchi


register = template.Library()

@register.simple_tag()
def total_posts():
    return Post.published.count()

@register.simple_tag()
def total_comments():
     return Comment.objects.filter(active=True).count()

@register.simple_tag() #mokhafaf name bjayeh funcname
def last_post():
    return Post.published.last().publish

@register.simple_tag
def popular_posts(count=4):
     return Post.published.annotate(comments_count=Count('comments')).order_by("-comments_count")[:count]

@register.inclusion_tag('partials/lastest_post.html')
def lastest_posts(count=4):
    l_posts = Post.published.order_by("-publish")[:count]
    context = {
    'l_posts':l_posts
    }
    return context

@register.filter(name="markdown")
def ls_markdown(text):
    return mark_safe(markdown(text))

@register.simple_tag
def max_readingtime_post(count=4):
    return Post.published.annotate(readingtime_max=Max('reading_time')).order_by("-readingtime_max")[:count]

@register.inclusion_tag("partials/bestuser.html")
def bestuser(count=3):
    best_users = User.objects.annotate(bestuser=Count("user_posts")).order_by("-bestuser")[:count]

    context = {
        "bestusers": best_users
    }
    return context

# @register.filter()
# def sansor(text):
#     return mark_safe(Sansorchi.remove_bad_words(text))