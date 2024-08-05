from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .forms import *
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery, TrigramSimilarity
from django.views.decorators.http import require_POST
from itertools import chain
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView

# Create your views here.


def index(request):
    return render(request, "blog/index.html")

def post_list(request, category=None):
    if category is not None:
        posts = Post.published.filter(category=category)
    else:
        posts = Post.published.all()
    paginator = Paginator(posts, "2")
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    context = {
        'posts': posts,
        'category': category
    }
    return render(request, "blog/list.html", context)
# class PostList(ListView):
#     queryset = Post.published.all()
#     paginate_by = 3
#     context_object_name = "posts"
#     ordering = "-publish"
#     template_name = "blog/list.html"


def post_details(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    form = CommentForm()
    comments = post.comments.filter(active=True)
    # try:
    #     post = Post.published.get(id=id)
    # except:
    #     raise Http404("No post found")
    context = {
        "post": post,
        "form": form,
        "comments": comments
    }
    return render(request, "blog/details.html", context)
# class DetailPost(DetailView):
#     model = Post
#     # context_object_name = "post"
#     template_name = "blog/details.html"

def ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket_obj = Ticket.objects.create()
            cd = form.cleaned_data
            Ticket.objects.create(massage=cd['massage'], name = cd['name'],
                                  email=cd['email'], phone = cd['phone'],subject = cd['subject'])
            return redirect("blog:index")
    else:
        form = TicketForm()
    return render(request, "forms/ticket.html", {"form": form})


@require_POST
def post_comment(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        "post": post,
        'form': form,
        'comment': comment

        }
    return render(request, "forms/comment.html", context)


def search_posts(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            # search 1
            # results1 = Post.published.filter(title__icontains=query)
            # results2 = Post.published.filter(description__icontains=query)
            # results =   results1 | results2
            # results = Post.published.filter(Q(title__icontains=query) | Q(description__icontains=query)) #for filter use it in futuer
            # search 2
            # search_query = SearchQuery(query)
            # search_vector = SearchVector("title", "description", "slug")
            # results = Post.published.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=search_query).order_by('-rank')
            # search 3
            results1 = Post.published.annotate(similarty=TrigramSimilarity("title", query)).filter(similarty__gt=0.1)
            results2 = Post.published.annotate(similarty=TrigramSimilarity("description", query)).filter(similarty__gt=0.1)
            results3 = Image.objects.annotate(similarty=TrigramSimilarity("title", query)).filter(similarty__gt=0.1)
            results4 = Image.objects.annotate(similarty=TrigramSimilarity("description", query)).filter(similarty__gt=0.1)
            results_p = (results1 | results2).order_by("similarty")
            results_i = (results3 | results4).order_by("similarty")
            for posti in results_i:
                 results.append(posti.post)
            for postp in results_p:
                results.append(postp)
            poste = Post.published.filter(id=1)
            post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")

            # print(request.user.id)
            # print(poste[0])

            print(User(User.objects.filter(id=1)).get_username())
            print(User.objects.filter(user_posts=poste[0]))
    context = {
        'query': query,
        'results': results
    }
    return render(request,  'forms/searchform.html', context)



@login_required
def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    comments = Comment.objects.filter(post=posts[1])
    paginator = Paginator(posts, "2")
    page_number = request.GET.get("page", 1)
    posts = paginator.page(page_number)
    context = {
        "posts": posts,
        "comments": comments
    }
    return render(request, "blog/profile.html", context)


@login_required
def create_posts(request):
    if request.method == "POST":
        form = CreatPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect("blog:post-list")
    else:
        form = CreatPostForm()
    return render(request, "forms/createpost.html", {"form": form})



def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('blog:profile')
    return render(request, "forms/delete-post.html", {"post": post})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CreatPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            Image.objects.create(image_file=form.cleaned_data['image1'], post=post)
            Image.objects.create(image_file=form.cleaned_data['image2'], post=post)
            return redirect("blog:profile")
    else:
        form = CreatPostForm(instance=post)
        return render(request, "forms/createpost.html", {"form": form, "post": post})


@login_required
def delete_image(request, img_id):
    img = get_object_or_404(Image, id=img_id)
    img.delete()
    return redirect("blog:profile")

# def login_user(request):
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd["username"], password=cd["password"])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect("blog:profile")
#                 else:
#                     return HttpResponse("your account is disable")
#             else:
#                 return HttpResponse("you are not login ")
#     else:
#         form = LoginForm()
#         print(dir(request.user))
#     return render(request, "registration/login.html", {"form": form})


def logout_user(request):
    logout(request)
    return redirect("blog:post-list")
    # return redirect(request.META.get("HTTP_REFERER")) #bargasht be safehe ghabli

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            Account.objects.create(user=user)
            return render(request, "registration/register_done.html", {"user": user})
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def edit_user(request):
    if request.method == "POST":
        user_form = UserEditForm(request.POST, instance=request.user)
        account_form = AccountEditForm(request.POST, instance=request.user.account, files=request.FILES)
        if user_form.is_valid() and account_form.is_valid():
            account_form.save()
            user_form.save()
            return redirect("blog:profile")
    else:
        user_form = UserEditForm(instance=request.user)
        account_form = AccountEditForm(instance=request.user.account)
    context = {
        "user_form": user_form,
        "account_form": account_form
    }

    return render(request, "registration/edit_account.html", context)


def user_detail(request, author):
    user = User.objects.get(username=author)
    posts = Post.published.filter(author=user)
    print(posts,user)
    context = {
        "user": user,
        "posts": posts
    }
    return render(request, "blog/user-detail.html", context)


class LoginViews(LoginView):
    next_page = "/blog"
    template_name = "registration/login.html"







