from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from apps.todos.serializers.todo_serializers import (
    TodoSerializers,
    TodoDestroySerializer,
)
from apps.todos.models import Todo
from apps.todos.pagination import TodoPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view


class TodoDestroyAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TodoDestroySerializer

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.destroy(serializer.validated_data)
        return Response(
            "todo has deleted",
            status=status.HTTP_200_OK,
        )


class TodoListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializers
    pagination_class = TodoPagination

    def create(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data, context={"user": user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def list(self, request):
        limit = 10
        data = self.get_queryset()
        paginator = self.pagination_class(limit)
        queryset = paginator.paginate_queryset(data, request)
        serialzer = TodoSerializers(queryset, many=True)

        return paginator.get_paginated_response(serialzer.data)

    def get_queryset(self):
        user = self.request.user
        queryset = Todo.objects.filter(creator=user, is_delete=False).order_by(
            "-created_at"
        )

        return queryset


class TodoRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TodoSerializers
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializers = self.get_serializer(instance)

        return Response(serializers.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializers = self.get_serializer(instance, request.data)
        serializers.is_valid(raise_exception=True)
        self.perform_update(serializers)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        user = self.request.user
        queryset = Todo.objects.filter(creator=user, is_delete=False)
        return queryset


# class TodoDestroyAPIView(generics.DestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     # serializer_class = TodoDestroySerializer

#     # def destroy(self, request, *args, **kwargs):
#     #     # serializer = self.get_serializer(data=request.data)
#     #     # serializer.is_valid(raise_exception=True)
#     #     # serializer.destroy(serializer.validated_data)

#     #     return Response(
#     #         "Todo is deleted",
#     #         status=status.HTTP_200_OK,
#     #     )
