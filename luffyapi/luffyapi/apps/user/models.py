from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    mobile = models.CharField(max_length=11,verbose_name='手机号')
    # 需要pillow模块的支持
    icon = models.ImageField(upload_to='icon',default='icon/default.png',verbose_name='头像',help_text='60x60')
    class Meta:
        db_table = 'luffy_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.username