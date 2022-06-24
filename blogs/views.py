from contextlib import ContextDecorator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import BlogPost, Comment, User, FollowersCount
from .forms import BlogPostForm, CommentForm

# Create your views here.
def index(request):
    """The home page for Blog"""
    return render(request, 'blogs/index.html')

def posts(request):
    """Show all posts"""
    posts = BlogPost.objects.order_by('-date_added')
    context = {'posts' : posts}
    return render(request, 'blogs/posts.html', context)

def post(request, post_id):
    """Show a single post and it's text/comments"""
    post = BlogPost.objects.get(id=post_id)
    
    comments = post.comment_set.order_by('-date_added')
    context = {'post': post, 'comments': comments}
    return render(request, 'blogs/post.html', context)

@login_required
def new_post(request):
    """Add a new post"""
    
    if request.method != 'POST':
        # No data submitted, create a blank form
        form = BlogPostForm()
    else:
        # POST submitted, process data
        form = BlogPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return redirect('blogs:posts')
    
    # Display a blank or invalid form
    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)

@login_required
def new_comment(request, post_id):
    """Add a new comment"""
    post = BlogPost.objects.get(id=post_id)

    if request.method != 'POST':
        # No data submitted, create a blank form
        form = CommentForm()
    else:
        # POST submitted, process data
        form = CommentForm(data=request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.owner = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('blogs:post', post_id=post_id)
    
    # Display a blank or invalid form
    context = {'post': post, 'form': form}
    return render(request, 'blogs/new_comment.html', context)

@login_required
def edit_post(request, post_id):
    """Edit an existing post"""
    post = BlogPost.objects.get(id=post_id)

    check_topic_owner(request, post)

    if request.method != 'POST':
        # Initial request, pre-fill form with current entry
        form = BlogPostForm(instance=post)
    else:
        # POST data submitted, process data
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:post', post_id=post.id)
    
    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)

def user_page(request, userpage_id):
    """Displaying a user's personal page"""

    # Get the username of the page's owner
    userpage = User.objects.get(username=userpage_id)
    logged_in = request.user.username

    # Get a list the number of followers and following the user has
    user_followers = len(FollowersCount.objects.filter(user=userpage.username))
    user_following = len(FollowersCount.objects.filter(follower=userpage.username))

    # Make a list of users that are following the page's user
    user_followers_list = FollowersCount.objects.filter(user=userpage.username)
    user_followers_true_list = []
    for i in user_followers_list:
        user_followers_list = i.follower
        user_followers_true_list.append(user_followers_list)

    # Make a list of users that this page's user follows
    user_following_list = FollowersCount.objects.filter(follower=userpage.username)
    user_following_true_list = []
    for i in user_following_list:
        user_following_list = i.user
        user_following_true_list.append(user_following_list)

    # If the logged in user is in the following list let them unfollow, let them follow otherwise
    if logged_in in user_followers_true_list:
        follow_button_value = 'unfollow'
    else:
        follow_button_value = 'follow'

    # Get the posts this user has made
    posts = BlogPost.objects.filter(owner=User.objects.get(username=userpage_id)).order_by('-date_added')

    context = {
        'userpage': userpage, 'posts': posts,
        'user_followers': user_followers,
        'user_following': user_following,
        'follow_button_value': follow_button_value,
        'user_followers_list': user_followers_true_list,
        'user_following_list': user_following_true_list,
        }
    return render(request, 'blogs/user_page.html', context)

@login_required
def followers_count(request):
    """Let user follow or unfollow"""
    if request.method == 'POST':
        # Getting these values from the buttons named ['name']
        value = request.POST['value']
        user = request.POST['user']
        follower = request.POST['follower']
        if value == 'follow':
            follower_cnt = FollowersCount.objects.create(follower=follower, user=user)
            follower_cnt.save()
        else:
            follower_cnt = FollowersCount.objects.get(follower=follower, user=user)
            follower_cnt.delete()

        return redirect('/'+user)

@login_required
def following(request):
    """Brings user to page of posts from users they follow"""
    logged_in = request.user.username

    user_following_list = FollowersCount.objects.filter(follower=logged_in)

    # Make a list of the usernames
    user_following_true_list = []
    for i in user_following_list:
        user_following_list = i.user
        user_following_true_list.append(user_following_list)

    users = User.objects.filter(username__in=user_following_true_list)
    posts = BlogPost.objects.filter(owner__in=users).order_by('-date_added')

    context = {'posts': posts}
    
    return render(request, 'blogs/following.html', context)



# Make sure user associated with topic is the current user
def check_topic_owner(request, post):
     if post.owner != request.user:
        raise Http404