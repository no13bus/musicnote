from django.db import models
from django.contrib.auth.models import User
import datetime
# Create your models here.

# python manage.py validate
# python manage.py sqlall books
# python manage.py syncdb
# python manage.py shell

# python manage.py shell 
# >>> from books.models import Publisher
# >>> p1 = Publisher(name='Apress', address='2855 Telegraph Avenue',
# ...     city='Berkeley', state_province='CA', country='U.S.A.',
# ...     website='http://www.apress.com/')
# >>> p1.save()

class Userprofile(models.Model):
	user = models.OneToOneField(User)
	nickname = models.CharField(max_length=30,default="")
	# avatar = models.ImageField(upload_to='./')
	avatar = models.CharField(max_length=40,default="")
	signature = models.CharField(max_length=100,default="")
	website = models.URLField()
	location = models.CharField(max_length=30,default="")
	role = models.CharField(max_length=30,default="")
	balance = models.IntegerField(max_length=11,default=0)
	reputation = models.IntegerField(max_length=11,default=0)
	self_intro = models.CharField(max_length=100,default="")
	created = models.DateField(blank=True,default=datetime.datetime.now().date()) 
	updated = models.DateField(blank=True,default=datetime.datetime.now().date()) 
	twitter = models.CharField(max_length=30,default="")
	github = models.CharField(max_length=30,default="")
	douban = models.CharField(max_length=30,default="")
	last_login = models.DateField(blank=True,default=datetime.datetime.now().date())
	def username(self):
		if self.nickname:
			return self.nickname
		else:
			return self.user.username
	def __unicode__(self):
		return self.signature

class Plane(models.Model):
	name = models.CharField(max_length=30,default="")
	created = models.DateField(blank=True,default=datetime.datetime.now().date()) 
	updated = models.DateField(blank=True,default=datetime.datetime.now().date()) 

	def __unicode__(self):
		return self.name

class Node(models.Model):
	name = models.CharField(max_length=30,default="")
	slug = models.CharField(max_length=30,default="")
	thumb = models.CharField(max_length=30,default="")
	introduction = models.CharField(max_length=30,default="")
	created = models.DateField(blank=True,default=datetime.datetime.now().date()) 
	updated = models.DateField(blank=True,default=datetime.datetime.now().date()) 
	plane = models.ForeignKey(Plane)
	topic_count = models.IntegerField(max_length=11,default=0)
	custom_style = models.CharField(max_length=30,default="")
	limit_reputation = models.IntegerField(default=10000)
	users = models.ManyToManyField(User)

	def __unicode__(self):
		return self.name

class Topic(models.Model):
	title = models.CharField(max_length=140,default="")
	content = models.CharField(max_length=500,default="")
	status = models.IntegerField(max_length=11,default=0)
	hits = models.IntegerField(max_length=11,default=0)
	created = models.DateField(blank=True,default=datetime.datetime.now().date()) 
	updated = models.DateField(blank=True,default=datetime.datetime.now().date()) 
	node = models.ForeignKey(Node)
	author = models.ForeignKey(User,related_name="author")
	reply_count = models.IntegerField(max_length=11,default=0)
	last_replied_by = models.ForeignKey(User,related_name="last_replied_by",blank=True, null=True)
	last_replied_time = models.DateField(blank=True,default=datetime.datetime.now().date()) 
	up_vote = models.IntegerField(max_length=11,default=0)
	down_vote = models.IntegerField(max_length=11,default=0)
	last_touched = models.DateField(blank=True,default=datetime.datetime.now().date()) 
	
	def __unicode__(self):
		return self.author.username

class Reply(models.Model):
	content = models.CharField(max_length=500,default="")
	topic = models.ForeignKey(Topic)
	author = models.ForeignKey(User)
	created = models.DateField(blank=True,default=datetime.datetime.now().date()) 
	updated = models.DateField(blank=True,default=datetime.datetime.now().date()) 
	up_vote = models.IntegerField(max_length=11,default=0)
	down_vote = models.IntegerField(max_length=11,default=0)
	last_touched = models.DateField(blank=True,default=datetime.datetime.now().date()) 


	def __unicode__(self):
		return self.author.username

class Message(models.Model):
	content = models.CharField(max_length=500,default="")
	status = models.IntegerField(max_length=11,default=0)
	from_user = models.ForeignKey(User,related_name='fromuser')
	to_user = models.ForeignKey(User,related_name='touser')
	created = models.DateField(blank=True,default=datetime.datetime.now().date()) 

	def __unicode__(self):
		return self.from_user.username


class Follow(models.Model):
	followed = models.ForeignKey(User,related_name='followed_user')
	follower = models.ForeignKey(User,related_name='follower_user')
	created = models.DateField(blank=True,default=datetime.datetime.now().date()) 

	def __unicode__(self):
		return self.follower.username
		
class Collection(models.Model):
	user = models.ForeignKey(User,related_name='owneruser')
	topic = models.ForeignKey(Topic,related_name='ownerusertopic')
	created = models.DateField(blank=True,default=datetime.datetime.now().date())