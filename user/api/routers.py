from .views import DragProfileViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('dragprofiles', DragProfileViewSet)