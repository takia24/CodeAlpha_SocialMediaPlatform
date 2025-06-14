from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.text import slugify

from .models import Post, Comment, Like, Follow
from .forms import PostForm, CommentForm, SignUpForm

from django.http import HttpResponseForbidden
from django.contrib.auth import logout
from django.shortcuts import redirect

from django.shortcuts import render, redirect
from .forms import ProfileForm

from core.models import Profile, Follow
from django.shortcuts import render, get_object_or_404



def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')  # সব পোস্ট ঐ ইউজারের
    return render(request, 'profile.html', {'profile_user': user, 'posts': posts})




@login_required
def home(request):
    # Get all posts ordered by creation time (newest first)
    posts = Post.objects.all().order_by('-created_at')
    
    # Initialize form
    form = PostForm()
    
    # Handle POST request (new post submission)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    
    # Prepare context with posts, form, and user data
    context = {
        'posts': posts,
        'form': form,
        'user': request.user,  # Makes user profile accessible in template
    }
    
    return render(request, 'core/home.html', context)


@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    return render(request, 'core/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })





def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Auto-generate username from first + last name
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            base_username = slugify(f"{first_name}{last_name}")
            counter = 1
            username = base_username
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            user.username = username
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})




@login_required
def profile_view(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)

    followers = Follow.objects.filter(following=request.user).count()
    following = Follow.objects.filter(follower=request.user).count()

    posts = Post.objects.filter(author=request.user).order_by('-created_at')  # ✅ নিজের পোস্টগুলো আনো

    return render(request, 'core/profile.html', {
        'user_profile': profile,
        'followers': followers,
        'following': following,
        'posts': posts,  # ✅ টেমপ্লেটে পাঠাও
    })




@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # শুধু সেই ইউজার নিজের পোস্ট এডিট করতে পারবে
    if post.author != request.user:
        return redirect('home')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm(instance=post)

    return render(request, 'core/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
        return redirect('home')
    else:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    


def logout_view(request):
    logout(request)
    return redirect('login')




@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'core/edit_profile.html', {'form': form, 'user': request.user})





def view_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile

    followers = Follow.objects.filter(following=user).count()
    following = Follow.objects.filter(follower=user).count()

    posts = Post.objects.filter(author=user)

    return render(request, 'core/view_profile.html', {
        'profile_user': user,
        'user_profile': profile,
        'followers': followers,
        'following': following,
        'posts': posts
    })




@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if user_to_follow == request.user:
        # নিজেকে ফলো করা যাবে না
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )
    if not created:
        follow.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))






