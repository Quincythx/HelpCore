from rest_framework import viewsets
from .models import Category, Ticket, Comment, Attachment
from .serializers import CategorySerializer, TicketSerializer, CommentSerializer, AttachmentSerializer
from .permissions import IsAuthenticated, IsAdmin, CanAccessTicket

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdmin()]
        return [IsAuthenticated()]


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, CanAccessTicket]

    def get_queryset(self):
        user = self.request.user

        if user.role == user.Role.EMPLOYEE:
            return Ticket.objects.filter(employee=user)
        elif user.role == user.Role.IT_STAFF:
            return Ticket.objects.filter(assigned_to=user)
        elif user.role == user.Role.ADMIN:
            return Ticket.objects.all()

        return Ticket.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ticket_id = self.kwargs.get("ticket_pk")
        return Comment.objects.filter(ticket_id=ticket_id)

    def perform_create(self, serializer):
        ticket_id = self.kwargs.get("ticket_pk")
        serializer.save(author=self.request.user, ticket_id=ticket_id)


class AttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ticket_id = self.kwargs.get("ticket_pk")
        return Attachment.objects.filter(ticket_id=ticket_id)

    def perform_create(self, serializer):
        ticket_id = self.kwargs.get("ticket_pk")
        serializer.save(uploaded_by=self.request.user, ticket_id=ticket_id)