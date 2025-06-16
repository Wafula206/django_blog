from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import PostForm

# Check if user is admin/staff
def is_admin(user):
    return user.is_authenticated and user.is_staff

def post_list(request):
    posts = Post.objects.all().order_by('-created')
    return render(request, 'blogapp/post_list.html', {'posts': posts})

# Admin-only: create post
@login_required
@user_passes_test(is_admin)
def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('post_list')
    return render(request, 'blogapp/post_form.html', {'form': form})

# Admin-only: edit post
@login_required
@user_passes_test(is_admin)
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post_list')
    return render(request, 'blogapp/post_form.html', {'form': form})

# Admin-only: delete post
@login_required
@user_passes_test(is_admin)
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blogapp/post_detail.html', {'post': post})
