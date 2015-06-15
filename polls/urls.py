from django.conf.urls import url, patterns
from polls.views import index, register, booth, statistics
from polls import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # ex: /polls/,
     url(r'^index/', index.as_view()),

     url(r'^register/', register.as_view(), name  = 'register'),

     url(r'^statistics/', statistics.as_view(), name  = 'statistics'),
     url(r'^(?P<poll_id>\d+)/booth/', booth.as_view(), name  = 'booth'),
     
)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)