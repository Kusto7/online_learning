from rest_framework import viewsets, generics

from users.models import User
from users.serliazers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ ViewSet для модели пользователя
        users.models.User """
    serializer_class = UserSerializer
    queryset = User.objects.all()
