from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Post, Profile, Comment
from .forms import PostForm, ProfileForm, CommentForm


def is_admin(user):
    return user.is_authenticated and user.is_staff


def post_list(request):
    posts = Post.objects.all().order_by('-created')
    return render(request, 'blogapp/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all().order_by('-created')

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.post = post
                comment.save()
                return redirect('post_detail', pk=post.pk)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'blogapp/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })


@login_required
@user_passes_test(is_admin)
def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('post_list')
    return render(request, 'blogapp/post_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post_list')
    return render(request, 'blogapp/post_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')


def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-created')
    return render(request, 'blogapp/user_profile.html', {
        'profile_user': profile_user,
        'posts': posts
    })


@login_required
def edit_profile(request):
    # Always ensure the profile exists for the current user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'blogapp/profile_form.html', {'form': form})
