from rest_framework.routers import SimpleRouter

from store.views import BookViewSet

router = SimpleRouter()
router.register(r'', BookViewSet)

urlpatterns = []

urlpatterns += router.urls
