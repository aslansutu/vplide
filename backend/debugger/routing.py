from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/debugger/(?P<debug_name>\w+)/$", consumers.DebuggerConsumer.as_asgi()),
]
