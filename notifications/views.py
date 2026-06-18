from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Notification
from .serializers import NotificationSerializer
from .permissions import IsOwnerOnly


class NotificationViewSet(viewsets.ModelViewSet):

    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated, IsOwnerOnly]

    def get_queryset(self):

        queryset = Notification.objects.filter(user=self.request.user)

        # FILTERS
        is_read = self.request.query_params.get("is_read")

        if is_read is not None:
            queryset = queryset.filter(is_read=is_read)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # ---------------------------
    # MARK SINGLE AS READ
    # ---------------------------
    @action(detail=True, methods=["patch"])
    def mark_read(self, request, pk=None):

        notification = self.get_object()
        notification.is_read = True
        notification.save()

        return Response({"message": "Marked as read"})

    # ---------------------------
    # MARK ALL AS READ
    # ---------------------------
    @action(detail=False, methods=["patch"])
    def mark_all_read(self, request):

        Notification.objects.filter(
            user=request.user,
            is_read=False
        ).update(is_read=True)

        return Response({"message": "All notifications marked as read"})

    # ---------------------------
    # UNREAD COUNT
    # ---------------------------
    @action(detail=False, methods=["get"])
    def unread_count(self, request):

        count = Notification.objects.filter(
            user=request.user,
            is_read=False
        ).count()

        return Response({"unread_count": count})