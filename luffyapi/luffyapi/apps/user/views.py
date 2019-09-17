from rest_framework.views import APIView
import re
from utils.response import APIResponse
from libs.txm import get_code,send_sms
from django.core.cache import cache
from .throttles import SMSRateThrottle
from .import models,serializers
from settings.const import SMS_CODE_EXC

class SMSAPIView(APIView):
    throttle_classes = [SMSRateThrottle]
    def post(self,request,*args,**kwargs):
        mobile = request.data.get('mobile')
        if not mobile or not re.match(r'^1[3-9][0-9]$',mobile):
            return APIResponse(1,'手机号有误')
        code = get_code()
        result = send_sms(mobile,code,SMS_CODE_EXC // 60)
        if not result:
            return APIResponse(1,'短信发送失败')

        cache.set('%s_code' % mobile, code, SMS_CODE_EXC)

        return APIResponse(0,'短信发送成功')


class MobileAPIView(APIView):
    def get(self,request,*args,**kwargs):
        mobile = request.query_params.get('mobile')
        if not mobile:
            return APIResponse(1,'手机号必须提供')
        if not re.match(r'^1[3-9][0-9]{9}$', mobile):
            return APIResponse(1,'手机号有误')
        try:
            models.User.objects.get(mobile=mobile)
            return APIResponse(1,'手机号已注册')
        except:
            return APIResponse(0,'手机号未注册')


class RegisterAPIView(APIView):
    def post(self,request,*args,**kwargs):
        request_data = request.data
        request_data['username'] = request_data.get('mobile')
        user_ser = serializers.UserModelSerializer(data=request_data)
        if user_ser.is_valid():
            user_ser.save()
            return APIResponse(0,'注册成功',results=user_ser.data)
        else:
            return APIResponse(1,'注册失败',results=user_ser.errors)


from rest_framework_jwt.serializers import jwt_encode_handler,jwt_payload_handler
class LoginAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()
    def post(self,request,*args,**kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not (username and password):
            return APIResponse(1,'账号或密码必须写')
        if re.match(r'^1[3-9][0-9]{9}$', username):
            try:
                user = models.User.objects.get(mobile=username)
            except:
                return APIResponse(1,'该手机未注册')

        else:
            try:
                user = models.User.objects.get(username=username)
            except:
                return APIResponse(1,'该账号未注册')

        if not user.check_password(password):
            return APIResponse(1,'密码错误')
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return APIResponse(0,'ok',results={
            'username': user.username,
            'mobile': user.mobile,
            'token': token
        })


class LoginMobileAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()
    def post(selfo,request,*args,**kwargs):
        mobile = request.data.get('mobile')
        code = request.data.get('code')
        if not (mobile and code):
            return APIResponse(1,'手机号或验证码必须写')
        old_code = cache.get('%s_code' % mobile)
        if code != old_code:
            return APIResponse(1,'验证码错误')
        try:
            user = models.User.objects.get(mobile=mobile)
        except:
            return APIResponse(1,'该账号未注册')
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return APIResponse(0,'ok',results={
            'username': user.username,
            'mobile': user.mobile,
            'token': token
        })