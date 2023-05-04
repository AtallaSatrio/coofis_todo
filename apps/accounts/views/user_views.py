from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from apps.accounts.serializers.user_serializers import UserRetrieveSerializer
from rest_framework.response import Response


class UserRetrieveGenericAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRetrieveSerializer

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
