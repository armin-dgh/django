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

# Create your views here.


def index(request):
    return render(request, "blog/index.html")

# def post_list(request):
#     posts = Post.published.all()
#     paginator = Paginator(posts, "2")
#     page_number = request.GET.get("page", 1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#
#     context = {
#         'posts': posts
#     }
#     return render(request, "blog/list.html", context)
class PostList(ListView):
    queryset = Post.published.all()
    paginate_by = 3
    context_object_name = "posts"
    ordering = "-publish"
    template_name = "blog/list.html"


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
        "comments":comments
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
            Ticket.objects.create(massage = cd['massage'], name = cd['name'],
                                  email = cd['email'], phone = cd['phone'],subject = cd['subject'])
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

def profile(request):
    user = request.user
    posts = Post.published.filter(author=user)
    context = {
        "posts": posts
    }
    return render(request, "blog/profile.html", context)
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        post.delete()
        return redirect('blog:profile')
    return render(request, "forms/delete-post.html", {"post": post})
