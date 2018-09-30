from .serializers import PostSerializer
from rest_framework import generics
from .pagination import StandardResultsSetPageNumberPagination
from posts.models import Post


class PostListView(generics.ListAPIView):
    queryset = Post.objects.order_by('timestamp')
    serializer_class = PostSerializer
    pagination_class = StandardResultsSetPageNumberPagination


class PostDetialView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
