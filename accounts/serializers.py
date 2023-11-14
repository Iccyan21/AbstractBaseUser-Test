
# serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    # シリアライズされるフィールドを指
    class Meta:
        model = User
        fields = ['userid', 'nickname', 'password', 'password_confirm', 'comment']
        
    #　パスワード一致確認
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm', None)
        #Userモデルのクリエイト処理を呼び出す。
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    # idとpassを受け取る
    userid = serializers.CharField()
    #style={'input_type': 'password'}により、APIブラウザでパスワードフィールドがマスクされます。
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        userid = attrs.get('userid')
        password = attrs.get('password')

        if userid and password:
            user = authenticate(request=self.context.get('request'), username=userid, password=password)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "userid" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
    
#情報更新
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'comment']  # 更新したいフィールドをここにリストアップ

    def update(self, instance, validated_data):
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.save()
        return instance