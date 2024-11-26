from django.shortcuts import render,redirect

from django.views import View
from .models import Topic
from .forms import TopicForm

class IndexView(View):

    def get(self, request, *args, **kwargs):
        return render(request,"bbs/index.html")

    def post(self, request, *args, **kwargs):

        form    = TopicForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            print(form.errors)

        return redirect("bbs:index")

index   = IndexView.as_view()





from django.core.cache import cache
from django.http import StreamingHttpResponse
import json
import time

def generate_sse():
    while True:
    
        # 60秒間キャッシュする。
        topics = cache.get('topics')
        if not topics:
            topics = Topic.objects.all()
            cache.set('topics', topics, timeout=60)

        #topics = Topic.objects.all()

        dic_topics = []

        for topic in topics:
            dic = {}
            dic["id"]       = topic.id
            dic["comment"]  = topic.comment

            dic_topics.append(dic)

        yield f"data: { json.dumps( {'contents': dic_topics} ) }\n\n"

        time.sleep(1)



# ↑ は60秒経つまでキャッシュは更新されない
# そこで、データの保存・削除を検知して即キャッシュをし直すようにする。
# ↓ のようにsignalを使う 

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

@receiver(post_save, sender=Topic)
def update_cache_on_save(sender, instance, **kwargs):
    topics = Topic.objects.all()
    cache.set('topics', topics, timeout=60)

@receiver(post_delete, sender=Topic)
def update_cache_on_delete(sender, instance, **kwargs):
    topics = Topic.objects.all()
    cache.set('topics', topics, timeout=60)


class TopicStreamView(View):
    def get(self, request, *args, **kwargs):
        return StreamingHttpResponse(
            generate_sse(), content_type="text/event-stream"
        )

topic_stream = TopicStreamView.as_view()


