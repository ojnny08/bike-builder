from .models import Comments
from .serializer import CommentsSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status


class CommentViewSet(ViewSet):
    def list(self, request):
        comments = Comments.objects.select_related("user").order_by("-created_at")
        build = request.query_params.get("build")
        if build:
            comments = comments.filter(build_id=build)
        serializer = CommentsSerializer(comments, many=True, context={"request": request})
        return Response(serializer.data)

    def create(self, request):
        serializer = CommentsSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        build = serializer.validated_data["build"]
        role = Comments.Role.POSTER if build.user_id == request.user.id else Comments.Role.COMMENTER
        serializer.save(user=request.user, role=role)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        try:
            comment = Comments.objects.get(pk=pk, user=request.user)
        except Comments.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CommentsSerializer(comment, data=request.data, partial=True, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            comment = Comments.objects.get(pk=pk, user=request.user)
        except Comments.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

