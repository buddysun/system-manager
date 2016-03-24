from django import forms
from .models import Hostname
from .models import Uploads
from .models import Release
from .models import *

class CommForm(forms.ModelForm):
	class Meta:
		model = Hostname
		fields = ('ipaddr','port','commd','results')

class UploadsForm(forms.ModelForm):	
	class Meta:
		model = Uploads
		fields = ('filename','remoteIP','remoteDir')

class ReleaseForm(forms.Form):	
	zipname=forms.FileField()
	project_name=forms.ModelMultipleChoiceField(
		queryset=Projects.objects.order_by('name'),
		required=True,
		widget=forms.CheckboxSelectMultiple,
		)
	results=forms.CharField(
		required=False,
		widget=forms.Textarea(
			attrs={
			'placeholder':"结果展示",
			'style':"width:100%",
			}
			),
		)

class RollbackForm(forms.Form):
	project=forms.ModelChoiceField(
		queryset=Backup.objects.values_list('project_name',flat=True).distinct(),
		required=True,
		widget=forms.Select,
		)
	backfile=forms.ModelChoiceField(
		queryset=Backup.objects.values_list('backfile',flat=True).distinct().order_by('-id')[:0],
		required=True,
		widget=forms.Select(
			attrs={
			'initial':"no haha",
			}
			),
		)
	results=forms.CharField(
		required=False,
		widget=forms.Textarea(
			attrs={
			'placeholder':"结果展示",
			'style':"width:100%",
			}
			),
		)