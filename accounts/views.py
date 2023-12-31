from .serializers import UserSerializer,LoginSerializer,UserUpdateSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from .models import  User
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied
from .permissions import IsUserOrReadOnly
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
# views.py

from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserSerializer

#CreateAPIViewを使う理由は作成に特化してるから(別にAPIViewでもいい)
class CreateUserView(CreateAPIView):
    model = User
    serializer_class = UserSerializer

#詳細表示用のView
class UserDetailView(APIView):
    def get(self, request, userid):
        # ユーザ情報の取得
        user = User.objects.filter(userid=userid).first()

        if not user:
            # ユーザが存在しない場合
            return Response({"message": "No User found"}, status=404)

        response_data = {
            "message": "User details by userid",
            "user": {
                "userid": user.userid,
                "nickname": user.nickname,
                "comment": user.comment
            }
        }

        return Response(response_data, status=200)
    
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'userid': user.userid,
            'message': 'Login successful!'
        }, status=status.HTTP_200_OK)
    
# 情報更新
# RetrieveUpdateAPIViewを使う理由は更新に特化してるから(別にAPIViewでもいい)
# 指定されたオブジェクトを取得（Retrieve）し、更新（Update）するための機能
class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    lookup_field = 'userid'
    permission_classes = [IsUserOrReadOnly]

    def get_object(self):
        # URLからuseridを取得
        userid = self.kwargs.get('userid')
        try:
            # 対象のユーザーオブジェクトを取得
            user = User.objects.get(userid=userid)
        except User.DoesNotExist:
            # ユーザーが存在しない場合はNotFoundエラーを発生させる
            raise NotFound('A user with this userid does not exist.')

        # リクエストユーザーが対象のユーザーでない場合はPermissionDeniedエラーを発生させる
        if self.request.user != user:
            raise PermissionDenied("You do not have permission to update this user's profile.")

        return user


class DeleteAccountView(APIView):
    def post(self, request,userid):
        ## アカウントの削除処理
        try:
            user = User.objects.filter(userid=userid).first()
            user.delete()
        except User.DoesNotExist:
            raise Response("No User found")

        return Response({"message": "Account and user successfully removed"}, status=200)
        

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    lookup_field = 'userid'

    def get_object(self):
        obj = super().get_object()
        if obj != self.request.user:
            raise PermissionDenied("You can't delete another user's account.")
        return obj