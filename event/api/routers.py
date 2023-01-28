from .views import DragEventViewSet,ListEventViewSet
from rest_framework import routers

event_router = routers.DefaultRouter()
event_router.register('events', DragEventViewSet, basename='main')
event_router.register('list_events', ListEventViewSet, basename='list')

