#encoding=utf-8
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from models import *
from forms import *
import pprint
import os
import uuid
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

import urllib2
import urllib

import uuid
import hashlib
from PIL import Image
import StringIO
from lib.gravatar import Gravatar

def nodes(request):
	active_page = 'nodes'
	data={}
	planes = Plane.objects.all()
	data['active_page'] = active_page
	data['planes'] = planes
	data['request']	= request
	if request.user.is_authenticated():
		topics = request.user.author.all()
		replies = request.user.reply_set.all()
		
		data['topics'] = topics.count()
		data['replies'] = replies.count()
	
	return render_to_response('nodes.html',data,context_instance=RequestContext(request))

def users(request):
	active_page = 'users'
	data={}
	data['request']	= request
	data['active_page']	= active_page
	active_users = User.objects.order_by('last_login')
	recent_reg_user = User.objects.order_by('date_joined')
	data['recent_reg_user']=recent_reg_user
	data['active_users']=active_users

	return render_to_response('users.html',data,context_instance=RequestContext(request))

def member_info(request,member_name):
	data={}
	data['request'] = request
	data['member_dict'] = {'签名':'signature','网站':'website','城市':'location','个人简介':'self_intro'}
	data['follow_user_text'] = '+关注'
	member = User.objects.filter(username=member_name)
	if member:
		member = member[0]
		data['member'] = member
		topics = member.author.all()###author是related_name的字串
		replies = member.reply_set.all()
		data['topics'] = topics
		data['replies'] = replies

	else:
		HttpResponseRedirect('index')###这里面应该是导入到500页面 用户未找到的页面
	return render_to_response('member_info.html',data,context_instance=RequestContext(request))

def user_topics(request,member_name):
	data={}
	member = User.objects.get(username=member_name)
	data['request'] = request
	data['member'] = member	
	topics = Topic.objects.filter(author__username=member_name)
	data['topics'] = topics
	return render_to_response('user_topics.html',data,context_instance=RequestContext(request))

def user_collections(request,member_name):
	data={}
	return render_to_response('user_topics.html',data,context_instance=RequestContext(request))

@login_required
def followuser(request):
	return HttpResponseRedirect(reverse('topicview',args=(topic_id,)))

@login_required
def followtopic(request,topic_id):
	relation = Collection.objects.filter(user=request.user,topic=Topic.objects.get(id=topic_id))
	print 'ssssss'
	if relation:
		print 'ddd'
		relation.remove()
	else:
		c = Collection(user=request.user,topic=Topic.objects.get(id=topic_id))
		c.save()
	print 'ddd'
	return HttpResponseRedirect(reverse('topicview',args=(topic_id,)))


def user_replies(request,member_name):
	data={}
	member = User.objects.filter(username=member_name)
	data['request'] = request
	data['member'] = member	
	replies = Reply.objects.filter(author__username=member_name)
	data['replies'] = replies
	return render_to_response('user_replies.html',data,context_instance=RequestContext(request))



@login_required
def createmessage(request,to_member):
	data={}
	data['request'] = request
	data['to_member'] = to_member
	if to_member==request.user.username:
		HttpResponseRedirect(reverse('index'))
	form = MessageForm()
	user_messages = Message.objects.filter(Q(from_user__username=to_member,to_user__username=request.user.username)|Q(from_user__username=request.user.username,to_user__username=to_member))
	# pprint.pprint(user_messages)
	if user_messages:
		data['user_messages'] = user_messages
	if request.method=="POST":
		
		form = MessageForm(request.POST)
		if form.is_valid():
			content = form.cleaned_data['content']
			m = Message(content=content,from_user=request.user,to_user=User.objects.get(username=to_member))
			m.save()
			HttpResponseRedirect(reverse('createmessage',args=(to_member,)))		
	data['form'] = form
	return render_to_response('createmessage.html',data,context_instance=RequestContext(request))


def index(request):
	data={}
	active_page = 'index'
	data['active_page'] = active_page	
	data['request']	= request	
	return render_to_response('index.html',data,context_instance=RequestContext(request))

def signout(request):
	logout(request)
	return HttpResponseRedirect(reverse('index'))

###php是将文件自动保存到一个tmp文件夹里面 然后需要保存的时候 将tmp文件夹里面的文件保存到一个别的地方 php可以检测文件类型
###python则不一样 py如何检测文件类型呢

@login_required
def avatar(request):
	data={}	
	if request.method=='GET':
		form = AvatarForm()
		data['request'] = request
	else:
		form = AvatarForm(request.POST, request.FILES)
		if form.is_valid():
			# image=request.FILES.get('avatar')
			# image = form.cleaned_data['avatar']
			# request.user.userprofile.avatar = form.cleaned_data['avatar']			
			# request.user.userprofile.save()#这样的话 上传的文件没有改名字 并且吧文件的路径上传到了数据库里面
			#如何能打印这个对象 类似var_dump函数???
			image = form.cleaned_data['avatar']
			extension = os.path.splitext(image.name)[-1]#50000的意思是50k
			if image.size > 500000:
				messages.error(request,'文件过大')
			if (extension not in ['.jpg', '.png', '.gif']) or ('image' not in image.content_type):
				messages.error(request,'文件类型不对')
			user_id = request.user.id
	        avatar_name = "%s" % uuid.uuid5(uuid.NAMESPACE_DNS, str(user_id))
	        avatar_buffer = StringIO.StringIO(image.read())

	        avatar = Image.open(avatar_buffer)


	        # # crop avatar if it's not square
	        avatar_w, avatar_h = avatar.size
	        avatar_border = avatar_w if avatar_w < avatar_h else avatar_h
	        avatar_crop_region = (0, 0, avatar_border, avatar_border)
	        avatar = avatar.crop(avatar_crop_region)

	        avatar_96x96 = avatar.resize((96, 96), Image.ANTIALIAS)
	        avatar_48x48 = avatar.resize((48, 48), Image.ANTIALIAS)
	        avatar_32x32 = avatar.resize((32, 32), Image.ANTIALIAS)
	        avatar_96x96.save(settings.STATIC_ROOT + "avatar/b_%s.png" % avatar_name, "PNG")
	        avatar_48x48.save(settings.STATIC_ROOT + "avatar/m_%s.png" % avatar_name, "PNG")
	        avatar_32x32.save(settings.STATIC_ROOT + "avatar/s_%s.png" % avatar_name, "PNG")

	        request.user.userprofile.avatar = avatar_name
	        request.user.userprofile.save()

	        return HttpResponseRedirect(reverse('avatar'))#必须写上return

	data['form'] = form
	return render_to_response('avatar.html',data,context_instance=RequestContext(request))


@login_required
def gravatar(request):
	data={}
	avatar_name = "%s" % uuid.uuid5(uuid.NAMESPACE_DNS, str(request.user.id))
	email = request.user.email
	gravatar = Gravatar(email)
	avatar_96x96 = gravatar.get_image(size = 96, filetype_extension = False)
	avatar_48x48 = gravatar.get_image(size = 48, filetype_extension = False)
	avatar_32x32 = gravatar.get_image(size = 32, filetype_extension = False)
	urllib.urlretrieve(avatar_96x96, settings.STATIC_ROOT + "avatar/b_%s.png" % avatar_name)
	urllib.urlretrieve(avatar_48x48, settings.STATIC_ROOT + "avatar/m_%s.png" % avatar_name)
	urllib.urlretrieve(avatar_32x32, settings.STATIC_ROOT + "avatar/s_%s.png" % avatar_name)
	# 每个人根据其id数字生成唯一的头像名称 不管是自己上传的还是gravatar获得的
	request.user.userprofile.avatar = avatar_name
	request.user.userprofile.save()#保存更新时间 虽然人的头像还是以前额名字

	return render_to_response('avatar.html',data,context_instance=RequestContext(request))


def register(request):
	data={}
	if request.method=='GET':
		form=RegisterForm()
	else:
		form=RegisterForm(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			if not User.objects.filter(username=username):
				password=form.cleaned_data['password']
				email=form.cleaned_data['email']
				user=User.objects.create_user(email=email,username=username,password=password)
				u=Userprofile(user=user)
				u.save()
				return HttpResponseRedirect(reverse('signin'))
			else:
				messages.error(request,u'用户名已经存在')
	data['form']=form
	return render_to_response('register.html',data,context_instance=RequestContext(request))


@login_required
def setting(request):
	data={}	
	data['request']	= request
	if request.method=='GET':		
		form = SettingForm()
		form = SettingForm(initial={
			'signature':request.user.userprofile.signature,
			'location':request.user.userprofile.location,
			'website':request.user.userprofile.website,
			'github':request.user.userprofile.github,
			'douban':request.user.userprofile.douban,
			'self_intro':request.user.userprofile.self_intro,
			})
	else:
		form = SettingForm(request.POST)
		if form.is_valid():
			request.user.userprofile.signature = form.cleaned_data['signature']
			request.user.userprofile.location = form.cleaned_data['location']
			request.user.userprofile.website = form.cleaned_data['website']
			request.user.userprofile.github = form.cleaned_data['github']
			request.user.userprofile.douban = form.cleaned_data['douban']
			request.user.userprofile.self_intro = form.cleaned_data['self_intro']
			request.user.userprofile.save()
	data['form'] = form
	return render_to_response('setting.html',data,context_instance=RequestContext(request))

def signin(request):
	data={}
	data['request'] = request
	if request.user.is_authenticated():		
		return HttpResponseRedirect(request.GET.get('next',reverse('index')))#如果next没有 如何跳转到上一个url	
		
	if request.method=='GET':
		form = SigninForm()	
		data['form'] = form
		return render_to_response('signin.html',data,context_instance=RequestContext(request))
	else:
		form = SigninForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			# user = User.objects.get(email=email)#filter指的是集合 不是单个 get如果取得2个的话会报错 如果取得值为空也报错
			users = User.objects.filter(email=email)			
			if not users:
				messages.error(request, '没有该用户')	
			else:
				user_auth = authenticate(username=users[0].username,password=password)
				if user_auth is None:
					messages.error(request, '密码错误')					
				else:
					login(request, user_auth)					
					return HttpResponseRedirect(request.GET.get('next',reverse('index')))	
	data['form'] = form	
	return render_to_response('signin.html',data,context_instance=RequestContext(request))


def nodetopics(request,slug):
	data={}
	data['request'] = request
	node = Node.objects.get(slug=slug)
	data['node'] = node
	topics_list = Topic.objects.filter(node__slug=slug)#多表联合查询 牛叉

	paginator = Paginator(topics_list,10)
	page = (int)(request.GET.get('page','1'))
	try:
		topics = paginator.page(page)
	except PageNotAnInteger:
		topics = paginator.page(1)
	except EmptyPage:
		topics = paginator.page(paginator.num_pages)
	data['topics'] = topics
	data['follow_text'] = '+关注'
	if request.user.is_authenticated():
		if node.users.filter(username=request.user.username):
			data['follow_text'] = '-取消关注'
	return render_to_response('nodetopics.html',data,context_instance=RequestContext(request))

def follownode(request,slug):
	data={}
	node = Node.objects.get(slug=slug)
	if request.user.is_authenticated():
		if node.users.filter(username=request.user.username):
			node.users.remove(request.user)
		else:
			node.users.add(request.user)
	else:
		return HttpResponseRedirect(reverse('signin')+'?next=/f/node/'+slug)

	return HttpResponseRedirect(reverse('nodetopics',args=(slug,)))

@login_required
def createtopic(request,slug):
	data={}
	data['request'] = request

	if request.method=="GET":
		form = CreatetopicForm()
	else:
		form = CreatetopicForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			content = form.cleaned_data['content']
			nodes = Node.objects.filter(slug=slug)
			node = nodes[0]
			t = Topic(title=title,content=content,hits=1,node=node,author=request.user)
			t.save()
			topic_count = node.topic_count + 1
			nodes.update(topic_count=topic_count)
			return HttpResponseRedirect(reverse('nodetopics',args=(slug,)))
	data['form'] = form
	return render_to_response('createtopic.html',data,context_instance=RequestContext(request))


def topicview(request,topic_id):
	data={}
	topics = Topic.objects.filter(id=topic_id)
	topic = topics[0]
	hits = topic.hits
	hits = hits + 1
	Topic.objects.filter(id=topic_id).update(hits=hits)
	data['request'] = request
	data['topic'] = topic
	data['favorite_text'] = '加入收藏'

	relation = Collection.objects.filter(user=request.user,topic__id=topic_id)
	if relation:
		data['favorite_text'] = '取消收藏'

	form = ReplyForm()

	relies_list = Reply.objects.filter(topic=topic)
	paginator = Paginator(relies_list,5)
	page = (int)(request.GET.get('page','1'))
	try:
		replies = paginator.page(page)
	except PageNotAnInteger:
		replies = paginator.page(1)
	except EmptyPage:
		replies = paginator.page(paginator.num_pages)

	####出现错误了 不能刷新页面
	data['replies'] = replies
	if request.method=='POST':
		form = ReplyForm(request.POST)
		if form.is_valid():
			content = form.cleaned_data['content']
			reply = Reply(content=content,topic=topic,author=request.user)
			reply.save()
			reply_count = topic.reply_count + 1
			topics.update(reply_count=reply_count,last_replied_by=request.user,last_replied_time=datetime.datetime.now().date())
			HttpResponseRedirect(reverse('topicview',args=(topic_id,)))
	data['form'] = form
	return render_to_response('topicview.html',data,context_instance=RequestContext(request))

@login_required
def edittopic(request,topic_id):
	data={}
	data['request'] = request	
	topic = Topic.objects.get(id=topic_id)
	if topic.author.id != request.user.id:
		return HttpResponseRedirect(reverse('index'))#应该是返回上个url

	if request.method=="GET":
		form = EdittopicForm(initial={
			'title':topic.title,
			'content':topic.content,
			})
	else:
		form = EdittopicForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			content = form.cleaned_data['content']
			t = Topic.objects.filter(id=topic_id)###这种比之前的那种save更加高效 save是全部都要更新一次  update()方法会返回一个整型数值，表示受影响的记录条数
			t.update(title=title,content=content,updated=datetime.datetime.now().date())
			return HttpResponseRedirect(reverse('topicview',args=(topic_id,)))
	data['form'] = form
	return render_to_response('edittopic.html',data,context_instance=RequestContext(request))