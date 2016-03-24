from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#服务器列表
class Hostlist(models.Model):
	ip = models.CharField(unique=True,max_length=50)
	name = models.CharField(max_length=60,blank=True,null=True)
	def __str__(self):
		return self.ip

#命令执行
class Hostname(models.Model):
	user = models.ForeignKey(User,'username')
	ipaddr = models.ManyToManyField(Hostlist,'ip')
	port = models.IntegerField(default=22)
	commd = models.CharField(max_length=200)
	results = models.TextField(blank=True,null=True)
	exec_date = models.DateTimeField(default=timezone.now)
	def __str__(self):
		return self.ipaddr

#文件上传
class Uploads(models.Model):
	user = models.ForeignKey(User,'username')
	destIPs = models.CharField(max_length=200,blank=True,null=True)
	filename = models.FileField(upload_to = '/buddy/release/uploads')
	upload_time = models.DateTimeField(default=timezone.now)
	remoteIP = models.ManyToManyField(Hostlist)
	remoteDir = models.CharField(max_length=100,blank=True,null=True)
	remotefile = models.CharField(max_length=100,blank=True,null=True)
	def __str__(self):
		return self.filename

#项目
class Projects(models.Model):
	name = models.CharField(max_length=38,blank=True,null=True)
	ip = models.GenericIPAddressField(blank=True,null=True)
	port = models.IntegerField(default=22)
	script = models.CharField(max_length=100,default='/data/yunwei/shell/njw_update.sh')
	rollback_shell = models.CharField(max_length=100,default='/data/yunwei/shell/njw_rollback.sh')
	back_path = models.CharField(max_length=100,default='/data/backup/www/')
	def __str__(self):
		return self.name

#版本发布
class Release(models.Model):
	user = models.ForeignKey(User,'username')
	project_name = models.CharField(max_length=200,blank=True,null=True)
	filename = models.FileField(upload_to = '/buddy/release/uploads')
	release_time = models.DateTimeField(default=timezone.now)
	results = models.TextField(blank=True,null=True)
	def __str__(self):
		return self.project_name

#备份
class Backup(models.Model):
	project_name = models.CharField(max_length=200,blank=True,null=True)
	backfile = models.CharField(max_length=200,blank=True,null=True)
	def __str__(self):
		return self.backfile

#Rollback记录
class Rollback(models.Model):
	user = models.ForeignKey(User,'username')
	project_name = models.CharField(max_length=200,blank=True,null=True)
	backtofile = models.CharField(max_length=200,blank=True,null=True)
	rollback_time = models.DateTimeField(default=timezone.now)
	results = models.TextField(blank=True,null=True)
	def __str__(self):
		return self.project_name

















