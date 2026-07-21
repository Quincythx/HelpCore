from rest_framework_nested import routers
from .views import CategoryViewSet, TicketViewSet, CommentViewSet, AttachmentViewSet

router = routers.DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("tickets", TicketViewSet, basename="ticket")

tickets_router = routers.NestedDefaultRouter(router, "tickets", lookup="ticket")
tickets_router.register("comments", CommentViewSet, basename="ticket-comments")
tickets_router.register("attachments", AttachmentViewSet, basename="ticket-attachments")

urlpatterns = router.urls + tickets_router.urls