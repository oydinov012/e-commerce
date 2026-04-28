from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from apps.users.models import User
from api.serializer.user_app import RegisterSerializer, UserSeralizer
from api.paginations import MyCustomPaginator
from rest_framework.generics import CreateAPIView



class UserModeViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSeralizer
    permission_classes = [AllowAny]
    pagination_class = MyCustomPaginator


class RegisterApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer