from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *


class PostList(APIView):
    def get(self, request):
        posts = PostProfile.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListWithUserId(APIView):
    def get(self, request, user_id):
        try:
            posts = PostProfile.objects.get(author__id=int(user_id))
            serializer = PostSerializer(posts, many=False)
        except PostProfile.DoesNotExist:
            return Response()
        return Response(serializer.data)
