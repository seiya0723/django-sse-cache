# == This code was created by https://noauto-nolife.com/post/django-auto-create-models-forms-admin/ == #

from django import forms
from .models import Topic

class TopicForm(forms.ModelForm):
    class Meta:
        model	= Topic
        fields	= [ "comment" ]

