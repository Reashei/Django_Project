from django.contrib import admin
from .models import Idea, Vote

# Register your models here.
admin.site.register(Idea)
admin.site.register(Vote)