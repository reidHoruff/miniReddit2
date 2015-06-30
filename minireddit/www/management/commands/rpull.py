from django.core.management.base import BaseCommand, CommandError
from www.models import *
from django.core import serializers
import urllib
import urllib2
import json
import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def add_id_to_file(id):
    f = open("pulled", "a")
    f.write("%s\n" % id)
    f.close()

def read_json_page(url):
    print "requesting:", url
    sleep = 1
    fails = 0
    while True:
        try:
            aResp = urllib2.urlopen(url)
            return json.loads(aResp.read())
        except:
            print "failed..."
            time.sleep(sleep)
            sleep += 1
            fails += 1
            if fails >= 5:
                print "aborting %s" % url
                return None

def create_or_get_user(username):
    try:
        return User.objects.get(username=username)
    except:
        return User.objects.create_user(
                username,
                "%s@foo.com" % username,
                "pass2"
            )

def create_or_get_sub(sub, creator=User.objects.get(username='root')):
    subreddit, created = Sub.objects.get_or_create(name=sub, defaults={'creator': creator})
    return subreddit

def handle_comment(post, node, parent=None):
    assert node['kind'] == 't1' or node['kind'] == 'more'

    if node['kind'] != 't1': 
        return

    data = node['data']
    author = data['author']
    score = data['score']
    body = data['body']
    author_user = create_or_get_user(author)

    post.sub.subscribers.add(author_user)

    current_comment = Comment.objects.create(
            author=author_user,
            score=score,
            body=body,
            parent=parent,
            post=post,
            scraped=True
        )

    if node['data']['replies']:
        children = node['data']['replies']['data']['children']
        for child in children:
            handle_comment(post, child, current_comment)

def read_comments(post, link):
    data = read_json_page(link)

    if not data:
        return None

    root_comments = data[1]['data']['children']
    for child in root_comments:
        handle_comment(post, child)

def read_sub(sub, pulled, after=None):

    if after:
        data = read_json_page("http://reddit.com/r/%s/.json?count=25&after=%s" % (sub, after))
    else:
        data = read_json_page("http://reddit.com/r/%s/.json" % sub)

    if not data:
        return None

    children = data['data']['children']

    subreddit = create_or_get_sub(sub)

    """
    name id of the last post pulled
    """
    last_post_name = None

    for child in children:
        if child['kind'] != 't3':
            continue

        cdata = child['data']

        last_name = cdata['name']

        if cdata['id'] in pulled:
            print 'skipping', cdata['id']
            continue

        """
        if Post.objects.filter(reddit_id=cdata['id']).exists():
            post = Post.objects.filter(reddit_id=cdata['id'])
            Comment.objects.filter(post=post).delete()
            post.delete()
        """

        post = Post.objects.create(
                url=cdata['url'],
                title=cdata['title'],
                author=create_or_get_user(cdata['author']),
                score=cdata['score'],
                body=cdata['selftext'],
                sub=create_or_get_sub(sub),
                reddit_id=cdata['id'],
                is_self=cdata['is_self'],
                domain=cdata['domain'],
                nsfw=cdata['over_18'],
                reddit_name=cdata['name'],
                thumb=cdata['thumbnail'],
                scraped=True
        )

        if cdata['is_self']:
            post.url = post.reddit_url()
            post.save()

        """
        print cdata['domain']
        print cdata['url']
        print cdata['over_18']
        print cdata['subreddit']
        print cdata['author']
        print cdata['title']
        print cdata['selftext']
        print cdata['selftext_html']
        print cdata['score']
        print cdata['permalink']
        print cdata['id']
        print cdata['name']
        print
        """

        if not read_comments(post, "http://reddit.com%s.json" % cdata['permalink']):
            continue

        add_id_to_file(post.reddit_id)

    return last_name

class Command(BaseCommand):

    def handle(self, *args, **options):
        pulled = set()
        for line in open("pulled"):
            pulled.add(line.strip())

        to_pull = [
                'pics',
                'askreddit',
                'news', 
                'videos',
                'audiophile',
                'brewing',
                'linux',
                'movies',
                'truefilm',
                'wikipedia',
                'physics',
                'funny',
                'books',
                'dailyprogrammer',
                'programming',
                'politics',
                'djent',
                'beer',
                'whatcouldgowrong',
                'crappydesign',
                'changemyview',
                'history',
                'food',
                'art',
                'diy',
                'fitness',
                'gifs',
                'personalfinance',
                'iama',
                'sports',
                'space',
                'television',
                'documentaries',
                'music',
                ]

        #just incase duplicated...
        to_pull = list(set(to_pull))

        for sub in to_pull:
            last_post_name = None
            for _ in range(4):
                last_post_name = read_sub(sub, pulled, last_post_name)
                if not last_post_name:
                    break

