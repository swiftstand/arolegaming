from .views import DragProfileViewSet, AroleViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('dragprofiles', DragProfileViewSet)
router.register('arolegaming', AroleViewSet)