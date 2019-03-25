from django.db import models

# Create your models here.

from django.contrib.auth.models import User
import django.utils.timezone as timezone

class DataWebsite(models.Model):
    # name = models.CharField('网站来源', max_length=100, primary_key=True, editable=False)
    name = models.CharField('网站来源', max_length=100, primary_key=True)
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class DataRegion(models.Model):
    name = models.CharField('景区', max_length=100, primary_key=True)
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class DataSource(models.Model):
    # name = models.CharField('数据类型', max_length=100, primary_key=True, editable=False)
    name = models.CharField('数据类型', max_length=100, primary_key=True)
    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

class Project(models.Model):
    data_website = models.ForeignKey(DataWebsite,on_delete=models.CASCADE)
    data_region = models.ForeignKey(DataRegion,on_delete=models.CASCADE)
    data_source = models.ForeignKey(DataSource,on_delete=models.CASCADE)
    class Meta:
        unique_together = ('data_website','data_region','data_source')
    status = models.CharField('项目状态', max_length=10, default='stop', editable=False)
    created_time = models.DateTimeField('首次创建时间', default = timezone.now, editable=False)
    modified_time = models.DateTimeField('最后修改时间', auto_now=True)
    editor = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return '%s-%s-%s' % (self.data_website,self.data_region,self.data_source)

    def __unicode__(self):
        return '%s-%s-%s' % (self.data_website, self.data_region, self.data_source)
