from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import View
from .forms import login_form
from .forms import register_form
from .forms import choices_form
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from polls.models import Voter, Choice, Poll
import json

from django.utils import timezone

# Create your views here.
class index(View):
	
	form = login_form
	template_name = 'polls/index_f.html'
	poll_list = Poll.objects.all()

	def get(self, request):
		form = self.form
		return render(request, self.template_name, {'form':form})

	def post(self, request):
		form = self.form(request.POST)

		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username = username, password = password)
	
			if user is not None:
				if user.is_active:
					login(request, user)
					return render(request, 'polls/polls.html', {'poll_list': self.poll_list})
				else:
					return HttpResponse("Sorry your account is not active yet")
			else:
				return HttpResponseRedirect("Invalid password or username")

def check_time(time):
	if(time < 3 or time > 14):
		return True

def check_voted(poll_id, username):
	p = Poll.objects.get(id = poll_id)

	all_votedat = p.votedat_set.all()

	for c in all_votedat:
		if (c.user == username):
			return True
	return False


class booth(View):

	def get(self, request, poll_id):

		poll = Poll.objects.get(pk = poll_id)
		poll_list = Poll.objects.all()

		poll_list = Poll.objects.exclude(id = poll_id)
		return render(request, 'polls/booth.html', {'poll': poll})

	def post(self, request, poll_id):
		p = get_object_or_404(Poll, pk=poll_id)

		poll_list = Poll.objects.exclude(id = poll_id)
		
		if request.user.is_authenticated():
			username = request.user.username
			print username

			try:
			    selected_choice = p.choice_set.get(pk=request.POST['choice'])
			except (KeyError, Choice.DoesNotExist):
			    # Redisplay the poll voting form.
			    return render(request, 'polls/detail.html', {
			        'poll': p,
			        'error_message': "You didn't select a choice.",
			    })

			else:

				time = timezone.now().hour
				if(check_time(time) == False):
					return HttpResponse("Sorry you are late to vote")
				elif(check_voted(poll_id, username) == True):
					return HttpResponse("Sorry you cannot vote twice")
				else:

					s = p.votedat_set.create(user = username, time = timezone.now())
					s.save()
					selected_choice.votes += 1
					selected_choice.save()
					# with POST data. This prevents data from being posted twice if a
					# user hits the Back button.
					#return HttpResponse("You logged out!")
					return render(request, 'polls/voted.html', {'poll_list': poll_list})

def check_age(age):
	if(age < 18):
		return False

class register(View):

		form = register_form()
		initial = {'key' : 'value'}
		template_name = 'polls/yo.html'

		def get(self, request):
			form = register_form
			return render(request, self.template_name, {'form': form})

		def post(self, request):
				form = register_form

				username = request.POST.get('username', False)
				password = request.POST.get('password', False)
				gender 	 = request.POST.get('gender', False)
				age		 = request.POST.get('age', False)
				
				if (check_age(int(age)) == False):
						return HttpResponse("Not eligible")

				else:

					user = User.objects.create_user(username, 'rishabhranawat@yahoo.com', password)
					user.save()

					v = Voter(voter_username = username, voter_gender = gender, voter_age = age)
					v.save()
					return HttpResponse("Created")



class statistics(View):

	def get(self, request):

		all_polls = Poll.objects.all()
		poll_1 = all_polls[0]
		poll_2 = all_polls[1]
		poll_3 = all_polls[2]

		choices_1 = poll_1.choice_set.all()
		choices_2 = poll_2.choice_set.all()
		choices_3 = poll_3.choice_set.all()

		all_voters = Voter.objects.filter(voter_gender = 'f')

		votes1 = []
		votes2 = []
		votes3 = []
		choices_all_1 = []

		for c in choices_1:
			votes1.append(c.votes)
			choices_all_1.append(str(c.choice_name))

		for c in choices_2:
			votes2.append(c.votes)

		for c in choices_3:
			votes3.append(c.votes)

		choices_all = json.dumps(choices_all_1) 
		print votes1, votes2, votes3

		return render(request, 'polls/examples/3d-column-interactive/stats.html', {'votes1': votes1, 'votes3': votes3, 'votes2': votes2, 
			'choices_all':choices_all})


def random_polls(number):

	for i in range(0, number, 1):
		name = "Poll"+ str(i)
		p = Poll(poll_name = name)
		p.save()

def random_users(number):

	for i in range(0, number, 1):
		name = "User"+ str(i)
		u = User(username = name, email = "rishabhranawat@yahoo.com", password = "word")
		u.save()

def random_voters():

	all_users = User.objects.all()
	i = 0
	for u in all_users:
		i = i+1
		username = u.username
		age = 40
		if(i%5 == 0):
			gender = 'f'
		else:
			gender = 'm'

		v = Voter(voter_username = username, voter_gender = gender, voter_age = age)
		v.save()


def random_votes():
	polls_list = Poll.objects.all()

	for p in polls_list:
		p.choice_set.create(choice_name = 'A', votes = 65)
		p.choice_set.create(choice_name = 'B', votes = 30)
		p.choice_set.create(choice_name = 'C', votes = 32)
