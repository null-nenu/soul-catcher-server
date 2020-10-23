from django.http import response
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from src.api.user.serializers import UserSerializer

# Create your views here.


class WechatViewSet(viewsets.GenericViewSet):
    @action(detail=False)
    def test(self, request):
        return Response({"msg": "test msg"})

    @action(detail=False, methods=["post"])
    def wechat_login(self, request):
        app_id = "wxac99fda59bb60d16"
        app_secret = "d231fbd0b536e856b7126f683ceb52c7"
        if not "code" in request.data:
            return Response({"msg": "error"}, status=500)
        else:
            code = request.data.get("code")
        session_key, openid = self._get_session_key(app_id, app_secret, code)
        if session_key != None and openid != None:
            user, _ = User.objects.get_or_create(
                username=openid
            )
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"msg": "登录失败，请重试。"}, status=500)

    def _decrypt_user_info(self, user_info: dict):
        app_id = "wxac99fda59bb60d16"
        app_secret = "d231fbd0b536e856b7126f683ceb52c7"

    def _get_session_key(self, app_id: str, app_secret: str, code: str):
        url = f"https://api.weixin.qq.com/sns/jscode2session?appid={app_id}&secret={app_secret}&js_code={code}&grant_type=authorization_code"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            return data.get("session_key", None), data.get("openid", None)
        else:
            return None, None
