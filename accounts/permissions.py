# permissions.py

from rest_framework import permissions

class IsUserOrReadOnly(permissions.BasePermission):
    """
    オブジェクトレベルの権限で、ユーザーが自分自身の情報のみ更新できるようにする。
    読み取りは全ユーザーに許可する。
    """

    def has_object_permission(self, request, view, obj):
        # 読み取りメソッドは常に許可
        if request.method in permissions.SAFE_METHODS:
            return True

        # 書き込み権限はそのユーザー自身にのみ許可
        return obj.userid == request.user.userid
