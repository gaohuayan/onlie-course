import os,django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'luffyapi.settings.dev')
django.setup()

from apps.home import models,serializers
banner_query = models.Banner.objects.all()
banner_ser = serializers.BannerModelSerializer(banner_query,many=True)
banner_data = banner_ser.data
print(banner_data)

from django.core.cache import cache
cache.set('banner_data',banner_data,10)
print(cache.get('banner_data'))
