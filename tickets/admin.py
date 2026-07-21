from django.contrib import admin
from .models import Category, Ticket, Comment, Attachment

admin.site.register(Category)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Attachment)
