from django.contrib import admin
from polls.models import Choice, Poll, Voter, VotedAt

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name of Poll',     {'fields': ['poll_name']}),
        ('Number of voters', {'fields': ['poll_votes'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)
admin.site.register(Voter)
admin.site.register(VotedAt)