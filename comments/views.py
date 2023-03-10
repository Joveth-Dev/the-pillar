from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from . serializers import CommentSerializer, ReplySerializer
from . models import Comment, Reply


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}


class ReplyViewSet(ModelViewSet):
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reply.objects.select_related('comment').filter(comment_id=self.kwargs['comment_pk'])

    def get_serializer_context(self):
        return {'user_id': self.request.user.id}
