from rest_framework import serializers
from .models import Category, Comment, Attachment, Ticket


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "default_assignee"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "ticket", "author", "message", "created_at"]
        read_only_fields = ["author", "created_at"]


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ["id", "ticket", "file", "uploaded_by", "uploaded_at"]
        read_only_fields = ["uploaded_by", "uploaded_at"]



class TicketSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    employee_id_display = serializers.CharField(source="employee.employee_id", read_only=True)
    assigned_to_display = serializers.CharField(source="assigned_to.employee_id", read_only=True, allow_null=True)
    comments = CommentSerializer(many=True, read_only=True)
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "employee",
            "employee_id_display",
            "assigned_to",
            "assigned_to_display",
            "category",
            "category_name",
            "subject",
            "description",
            "department",
            "priority",
            "status",
            "created_at",
            "updated_at",
            "comments",
            "attachments",
        ]
        read_only_fields = ["employee", "assigned_to", "status", "created_at", "updated_at"]