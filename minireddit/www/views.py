from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from easy.decorators import *
from www.models import *
import forms

@context_template_response
def home(request):
    start = int(request.REQUEST.get('start', 0))
    defaults = [
            'funny',
            'pics',
            'askreddit',
            'news',
            'movies',
            'books',
            'programming',
        ]

    if request.user.is_authenticated():
        posts = Post.objects.filter(sub__in=request.user.subscribed_to.all()).order_by('-score')[start:start+25]
    else:
        posts = Post.objects.filter(sub__name__in=defaults).order_by('-score')[start:start+25]

    data = {
            'form': forms.LoginForm(),
            'all_subs': Sub.objects.all(),
            'posts': posts,
            'is_sub': False,
            'start': start,
            'next': "/?start=%s" % (start+25),
            'prev': "/?start=%s" % (start-25),
        }
    return "home.html", data

def view_subreddit(request, subreddit):
    issubbed = request.user.is_authenticated() and Sub.objects.filter(name=subreddit, subscribers__id=request.user.id).exists()
    start = int(request.REQUEST.get('start', 0))

    data = {
            'issubbed': issubbed,
            'all_subs': Sub.objects.all(),
            'form': forms.LoginForm(),
            'posts': Post.objects.filter(sub=Sub.objects.get(name=subreddit))[start:start+25],
            'is_sub': True,
            'subscribers': Sub.objects.get(name=subreddit).subscribers.count(),
            'subreddit': subreddit,
            'start': start,
            'next': "/r/%s/?start=%s" % (subreddit, start+25),
            'prev': "/r/%s/?start=%s" % (subreddit, start-25),
        }

    return render_to_response(
            "home.html",
            data,
            context_instance=RequestContext(request)
        )

def view_post(request, subreddit, post_id):
    issubbed = request.user.is_authenticated() and Sub.objects.filter(name=subreddit, subscribers__id=request.user.id).exists()
    data = {
            'issubbed': issubbed,
            'all_subs': Sub.objects.all(),
            'form': forms.LoginForm(),
            'post': Post.objects.get(id=post_id),
            'is_sub': True,
            'subscribers': Sub.objects.get(name=subreddit).subscribers.count(),
            'subreddit': subreddit,
            'rootcommentform': forms.PostComment().set_parent_id(-1).set_post_id(post_id),
            }

    return render_to_response(
            "post.html",
            data,
            context_instance=RequestContext(request)
        )

@context_template_response
def register(request):
    return "register.html", {'form': forms.Register()}

@context_template_response
def submit(request):
    sub = request.REQUEST.get('sub')
    return "submit.html", {'form': forms.SubmitPost().set_sub(sub)}

@context_template_response
def create_sub(request):
    return "createsub.html", {'form': forms.CreateSub()}

@context_template_response
def _login(request):
    return "login.html", {'form': forms.LoginForm()}

def view_profile(request, username):
    data = {
            'owner': User.objects.get(username=username),
    }
    return render_to_response(
            "profile.html",
            data,
            context_instance=RequestContext(request)
        )
