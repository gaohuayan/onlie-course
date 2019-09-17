from rest_framework import serializers
from . import models
from django.core.cache import cache
import re
class UserModelSerializer(serializers.ModelSerializer):
    code = serializers.CharField(write_only=True, min_length=4, max_length=4)
    class Meta:
        model = models.User
        fields = ('username', 'password', 'mobile', 'code')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate_mobile(self, value):
        if not re.match(r'^1[3-9][0-9]{9}$', value):
            raise serializers.ValidationError('手机号有误')
        return value

    def validate(self, attrs):
        code = attrs.pop('code')
        mobile = attrs.get('mobile')
        old_code = cache.get('%s_code' % mobile)
        if code != old_code:
            raise serializers.ValidationError({'验证码': '验证码有误'})
        return attrs

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)


