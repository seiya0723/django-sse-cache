from django.contrib import admin

# Register your models here.
# == This code was created by https://noauto-nolife.com/post/django-auto-create-models-forms-admin/ == #

from django.contrib import admin
from .models import Topic

class TopicAdmin(admin.ModelAdmin):
    list_display	= [ "id", "comment" ]


admin.site.register(Topic,TopicAdmin)
