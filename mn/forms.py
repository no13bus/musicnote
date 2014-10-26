#encoding=utf-8

from django import forms
from models import *


class SigninForm(forms.Form):
	# forms.TextInput(attrs={'style':'border:1px solid #ccc;'}))
	email=forms.EmailField(required=True,error_messages={'required':u'邮箱必须','invalid':u'请输入正确的邮箱'},widget=forms.TextInput(attrs={'id':'email','class':'input-xlarge'}))
	password=forms.CharField(required=True,error_messages={'required':u'密码必须'},widget=forms.PasswordInput(attrs={'id':'password','class':'input-xlarge'}))

class RegisterForm(forms.Form):
	email=forms.EmailField(widget=forms.TextInput(attrs={'id':'email','class':'input-xlarge'}))
	password=forms.CharField(widget=forms.PasswordInput(attrs={'id':'password','class':'input-xlarge'}))
	username=forms.CharField(required=True,max_length='16',min_length='4',error_messages={'required':u'密码必须','max_length':u'用户名过长','min_length':u'用户名过短'},widget=forms.TextInput(attrs={'id':'username','class':'input-xlarge'}))
	
class SettingForm(forms.Form):
	#required=False必须要加上required默认是true
	signature=forms.CharField(required=False,error_messages={'max_length':u'个人签名过长'},widget=forms.TextInput(attrs={'id':'signature','class':'input-xlarge'}))
	location=forms.CharField(required=False,error_messages={'max_length':u'不合适的城市名字'},widget=forms.TextInput(attrs={'id':'location','class':'input-xlarge'}))
	website=forms.URLField(required=False,error_messages={'invalid':u'无效的网址'},widget=forms.TextInput(attrs={'id':'website','class':'input-xlarge'}))
	douban=forms.CharField(required=False,widget=forms.TextInput(attrs={'id':'douban','class':'input-xlarge'}))
	github=forms.CharField(required=False,widget=forms.TextInput(attrs={'id':'github','class':'input-xlarge'}))
	self_intro=forms.CharField(required=False,error_messages={'max_length':u'介绍太长'},widget=forms.Textarea(attrs={'id':'self_intro','class':'input-xlarge','rows':'10'}))

class AvatarForm(forms.Form):
	# max_length说的是模型里面的字段长度 也就是在数据库里面的长度
	avatar=forms.ImageField(max_length='50',error_messages={'required':u'文件必须','max_length':u'文件名过长','empty':u'文件大小为0','invalid_image':u'选择正确的图片文件'},widget=forms.FileInput(attrs={'id':'avatar','class':'input-xlarge'}))
	
class CreatetopicForm(forms.Form):
	title=forms.CharField(max_length='120',min_length='3',error_messages={'required':u'标题必须','min_length':u'帖子过短','max_length':u'标题控制在120字符内'},widget=forms.TextInput(attrs={'id':'title','class':'span11','placeholder':u'话题'}))
	content=forms.CharField(required=True,max_length='1000',error_messages={'required':u'内容必须','max_length':u'内容控制在1000字以内'},widget=forms.Textarea(attrs={'placeholder':u'编辑内容','id':'content','row':'3','class':'content mt5 smart-code-support'}))
		
class EdittopicForm(forms.Form):
	title=forms.CharField(required=True,error_messages={'required':u'标题必须'},widget=forms.TextInput(attrs={'id':'title','class':'span11','placeholder':u'话题'}))
	content=forms.CharField(required=True,error_messages={'required':u'内容必须'},widget=forms.Textarea(attrs={'placeholder':u'编辑内容','id':'content','row':'3','class':'content mt5 smart-code-support'}))
		
class ReplyForm(forms.Form):
	content=forms.CharField(required=True,error_messages={'required':u'回复内容必须'},widget=forms.Textarea(attrs={'id':'content','class':'content mt5 smart-code-support J_replyContent','row':'3','placeholder':u'回复内容'}))

class MessageForm(forms.Form):
	content=forms.CharField(required=True,error_messages={'required':u'私信内容必须'},widget=forms.Textarea(attrs={'id':'content','class':'content mt5 smart-code-support','row':'3','placeholder':u'输入私信内容','style':'width: 640px; height: 54px;'}))
