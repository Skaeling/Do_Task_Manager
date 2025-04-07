from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.permissions import IsUser, IsSupervisor
from users.serializers import UserCreateSerializer, UserRetrieveSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Создает новый профиль пользователя"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Отображает профиль пользователя, если он принадлежит текущему юзеру или если пользователь супервайзер"""
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = (IsUser | IsSupervisor,)


class UserUpdateAPIView(generics.UpdateAPIView):
    """Обновляет профиль текущего пользователя по переданному pk"""
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUser,)


class UserDeleteAPIView(generics.DestroyAPIView):
    """Удаляет профиль текущего пользователя по переданному pk"""
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated, IsUser,)
