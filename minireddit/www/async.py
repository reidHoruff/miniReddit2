from django.template import RequestContext
from django.http import *
from sniper.snipers import *
import sniper.decorators as sniper
from easy.decorators import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from models import *
import forms
from django.core.cache import cache
from urlparse import urlparse

defaults = [
        'pics',
        'videos',
        'askreddit',
        'news',
        'movies',
        'books',
        'programming',
    ]

@sniper.ajax()
def register(request):
    form = forms.Register(request.POST)

    if not form.is_valid():
        yield InsertText('#error', form.get_first_error()), None

    if form.cleaned_data['password1'] != form.cleaned_data['password2']:
        yield InsertText('#error', "Passwords do not match"), None

    pw = form.cleaned_data['password1']

    username  = form.cleaned_data['username']
    email = '%s@foobar.com' % form.cleaned_data['username']

    try:
        user = User.objects.create_user(
            username,
            email,
            pw
        )
    except:
        yield InsertText('#error', "username already exists :("), None

    user = authenticate(username=username, password=pw)

    for default in defaults:
        try:
            user.subscribed_to.add(Sub.objects.get(name=default))
        except:
            pass

    user.save()
    login(request, user)
    yield RedirectBrowser('/'), None

@sniper.ajax()
def submit(request):
    form = forms.SubmitPost(request.POST)

    if form.is_valid():
        title = form.cleaned_data['title']
        url = form.cleaned_data['url']
        subreddit = form.cleaned_data['subreddit']
        body = form.cleaned_data['body']
        nsfw = form.cleaned_data['body']

        if len(Sub.objects.filter(name=subreddit)) < 1:
            yield InsertText('#error', "subreddit not does not exist"), None

        if not url and not body:
            yield InsertText('#error', "you must supply either a url or body text."), None

        if not url:
            is_self = True
            domain = "self.%s" % subreddit
        else:
            is_self = False
            domain = '{uri.netloc}'.format(uri=urlparse(url))

        post = Post.objects.create(
            url=url,
            title=title,
            author=request.user,
            body=body,
            sub=Sub.objects.get(name=subreddit),
            score=1,
            is_self=is_self,
            domain=domain,
            nsfw=nsfw
        )

        if is_self:
            post.url = "/r/%s/post/%s/" % (subreddit, post.id)
            post.save()

        yield RedirectBrowser('/r/%s/post/%s/' % (subreddit, post.id)), None

    else:
        yield InsertText('#error', form.get_first_error()), None

@sniper.ajax()
def comment(request):
    form = forms.PostComment(request.POST)

    if form.is_valid():
        body = form.cleaned_data['body']
        post_id = form.cleaned_data['post_id']
        parent_id = form.cleaned_data['parent_id']

        post = Post.objects.get(id=post_id)

        parent = None
        if parent_id >= 0:
            parent = Comment.objects.get(id=parent_id)

        Comment.objects.create(
            author=request.user,
            body=body,
            parent=parent,
            score=1,
            post=post
        )

        cache_key = "post:%s" % post.id
        cache.delete(cache_key)

        yield RedirectBrowser('/r/%s/post/%s/' % (post.sub.name, post.id)), None

    else:
        yield InsertText('#error', form.get_first_error()), None

@sniper.ajax()
def _logout(request):
    if request.user.is_authenticated():
        logout(request)
    n = request.REQUEST.get('next')
    if n:
        yield RedirectBrowser(n)
    else:
        yield RedirectBrowser('/')

@sniper.ajax()
def _login(request):
    form = forms.LoginForm(request.POST)

    if form.is_valid():
        username  = form.cleaned_data['username']
        email = '%s@foobar.com' % form.cleaned_data['username']
        pw = form.cleaned_data['password']
        user = authenticate(username=username, password=pw)

        if user and user.is_active:
            login(request, user)
            yield RedirectBrowser('/'), None

    yield InsertText("#error", "Error with login credentials"), None

@sniper.ajax()
def create_sub(request):
    form = forms.CreateSub(request.POST)

    if form.is_valid():
        name  = form.cleaned_data['name']
        if len(Sub.objects.filter(name=name)) > 0:
          yield InsertText('#error', 'sub name already exists'), None

        Sub.objects.create(name=name, creator=request.user)
        yield RedirectBrowser('/r/%s/' % name), None
    else:
        yield InsertText('#error', form.get_first_error()), None

@sniper.ajax()
def view_comment_reply(request):
    if not request.user.is_authenticated():
        yield RedirectBrowser('/login/'), None

    parent_id = request.REQUEST['parent_id']
    post_id = request.REQUEST['post_id']

    args = {
            'commentform': forms.PostComment().set_parent_id(parent_id).set_post_id(post_id),
            'user': request.user,
    }

    yield InsertTemplate(".reply-box-%s"%parent_id, "replybox.html", args)

@sniper.ajax()
def getbody(request):
    post_id = request.REQUEST['post_id']

    args = {
            'post': Post.objects.get(id=post_id),
    }

    yield InsertTemplate(".body-insert-%s" % post_id, "body.html", args)

@sniper.ajax()
def showimg(request):
    post_id = request.REQUEST['post_id']
    post = Post.objects.get(id=post_id)
    img = """<img src="%s"></img>""" % post.url
    yield InsertText(".body-insert-%s" % post_id, img)

@sniper.ajax()
def vote(request):

    if not request.user.is_authenticated():
        yield RedirectBrowser('/login/'), None

    type = request.REQUEST.get('type')
    id = request.REQUEST.get('id')
    value = request.REQUEST.get('value')
    value = {'u': 1, 'd': -1}[value]

    if type == 'post':
        post = Post.objects.get(id=id)
        old_value = 0
        if PostVote.objects.filter(author=request.user, post=post).exists():
            vote = PostVote.objects.get(author=request.user, post=post)
            old_value = vote.value
            vote.value = value
            vote.save()
        else:
            PostVote.objects.create(
                    author=request.user,
                    post=post,
                    value=value
                    )
        post.score -= old_value
        post.score += value
        post.save()
        yield JSLog("score updated: %s" % post.score)
        yield InsertText("#score-%s" % id, post.score)

    if type == 'comment':
        comment = Comment.objects.get(id=id)
        old_value = 0
        if CommentVote.objects.filter(author=request.user, comment=comment).exists():
            vote = CommentVote.objects.get(author=request.user, comment=comment)
            old_value = vote.value
            vote.value = value
            vote.save()
        else:
            CommentVote.objects.create(
                    author=request.user,
                    comment=comment,
                    value=value
                    )
        comment.score -= old_value
        comment.score += value
        comment.save()
        yield InsertText("#comm_score_%s" % id, "%s points" % comment.score)
        yield JSLog("score updated: %s" % comment.score)

@sniper.ajax()
def subscribe(request):
    if not request.user.is_authenticated():
        yield RedirectBrowser('/login/'), None

    subreddit = request.REQUEST.get('sub')
    action = request.REQUEST.get('a')
    if action == 's':
        Sub.objects.get(name=subreddit).subscribers.add(request.user)
    elif action == 'u':
        Sub.objects.get(name=subreddit).subscribers.remove(request.user)
    yield RefreshBrowser(), None
