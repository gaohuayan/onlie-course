from rest_framework import serializers
from .models import Banner
class BannerModelSerializer(serializers.ModelSerializer):
    """轮播图序列化器"""
    class Meta:
        model = Banner
        # 序列化的目的就是反馈给外界，所以指定的字段就行，其他字段用于orm数据的筛选
        fields = ("image", "link")