from rest_framework.routers import SimpleRouter
from events.views import EventViewSet

router = SimpleRouter()
router.register('events', EventViewSet)

urlpatterns = [
]