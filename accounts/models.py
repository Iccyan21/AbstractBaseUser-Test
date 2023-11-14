from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _

# 通常のユーザーとスーパーユーザーの両方を作成する能力を提供する
class UserManager(BaseUserManager): 
    #通常のUserを作成する
    def create_user(self, userid, password, nickname, **extra_fields):
        if not userid:
            raise ValueError(_('ユーザーIDは必須です。'))
        user = self.model(userid=userid, nickname=nickname, **extra_fields)
        #パスワードをハッシュ化
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    #管理者ユーザーを作成する
    def create_superuser(self, userid, password, nickname, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(userid, password, nickname, **extra_fields)

#passwordはAbstractBaseUserに含まれているので、ここでは定義しない
class User(AbstractBaseUser,PermissionsMixin):
    userid = models.CharField(max_length=100, unique=True)
    nickname = models.CharField(max_length=100)
    comment = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    # 管理サイトにアクセスできるかどうか
    is_staff = models.BooleanField(default=False)
    
    # これはユーザーの作成（通常のユーザーとスーパーユーザー）を管理するために必要です。
    objects = UserManager()
    # useridがユーザー名の代わりに使用
    USERNAME_FIELD = 'userid'
    # 管理コマンドを使用してスーパーユーザーを作成する際に必要とされるフィールドのリスト
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.userid

# Create your models here.
