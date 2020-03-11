from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'ws/upload-csv/(?P<token>[^/]+)/$', consumers.UploadCSVConsumer),
]
