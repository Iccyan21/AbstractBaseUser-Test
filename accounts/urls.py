from . import views
from django.urls import path, include
from .views import CreateUserView, UserUpdateView,UserDeleteView

urlpatterns = [
    # path('signup/', views.RegisterView.as_view(), name='user-signup'), # 新規登録処理'
    path('signup/', CreateUserView.as_view(), name='signup'),
    path('login/', views.LoginAPIView.as_view(), name='user-login'), # ログイン処理
    path('users/<str:userid>/', views.UserDetailView.as_view(), name='user-detail'), # ユーザ情報取得
    path('users/<str:userid>/update/', UserUpdateView.as_view(), name='user-update'),
    #path('users/<str:user_id>/update/', views.UserUpdateView.as_view(), name='user-update'), # ユーザ情報更新
    path('delete/<str:userid>/', views.DeleteAccountView.as_view(), name='delete-account'), # アカウント削除
    path('users/<str:userid>/delete/', UserDeleteView.as_view(), name='user-delete'),
]