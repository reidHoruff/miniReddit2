from django.contrib import admin
from www.models import *

admin.site.register(Sub)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(CommentVote)
admin.site.register(PostVote)

