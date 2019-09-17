from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from .import models,serializers
from rest_framework.response import Response

# from .models import Banner
# from .serializers import BannerModelSerializer
# class BannerListAPIView(ListAPIView):
#     queryset = Banner.objects.filter(is_show=True, is_delete=False).order_by("-orders")
#     serializer_class = BannerModelSerializer

from django.core.cache import cache
class BannerListAPIView(ListAPIView):
    def get(self,request,*args,**kwargs):
        banner_list_data = cache.get('api_banner_list_data')
        if not banner_list_data:
            banner_query = models.Banner.objects.filter(is_show=True,is_delete=False).order_by('-orders')
            banner_list_data = serializers.BannerModelSerializer(banner_query,many=True).data
            cache.set('api_banner_list_data',banner_list_data)
        return Response(banner_list_data)