from django import forms
from polls.models import Choice

class login_form(forms.Form):
	username = forms.CharField(label = 'username', max_length = 200)
	password = forms.CharField(label = 'password', max_length = 200)

class register_form(forms.Form):
	username = forms.CharField(label = 'username', max_length = 200)
	password = forms.CharField(label = 'password', max_length = 200)
	gender	 = forms.CharField(label = 'gender', max_length = 2)
	age 	 = forms.IntegerField()

	def create_me(self, username, password, gender, age):
		user = User.objects.create_user(username, 'rishabhranawat@yahoo.com', password)
		user.save()
		print "created"


class choices_form(forms.Form):
	a= forms.ChoiceField(choices = Choice.objects.all(), widget = forms.RadioSelect())
