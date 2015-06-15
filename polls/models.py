from django.db import models
from django.utils import timezone

# Create your models here.

class Poll(models.Model):
	poll_name 		= models.CharField(max_length = 200)
	poll_votes 		= models.IntegerField(default = 0)

	#methods
	def __unicode__(self):
		return self.poll_name


class Choice(models.Model):
	poll 			= models.ForeignKey(Poll)
	choice_name 	= models.CharField(max_length = 200)
	votes 			= models.IntegerField(default = 0)

	#methods
	def __unicode__(self):
		return self.choice_name

class VotedAt(models.Model):

			poll = models.ForeignKey(Poll)
			user = models.CharField(max_length = 200)
			time = models.DateTimeField(default = timezone.now())

class Voter(models.Model):
	
	#Biometric Information
	voter_username	= models.CharField(max_length = 200)
	voter_gender 	= models.CharField(max_length = 1)
	voter_age 		= models.IntegerField(default = 0)

	#Voting+Analytics Related Information
	voter_votes = models.IntegerField(default = 0)
	
	voting_time = models.ForeignKey(VotedAt, blank = True, null = True)
	#methods
	def __unicode__(self):
		return self.voter_username














