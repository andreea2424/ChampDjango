# models.py
from django.utils import timezone
from django.db import models

class Team(models.Model):
    match_count = models.IntegerField(null=True, default=None)
    establishment_year = models.IntegerField(null=True, default=None)
    total_rating = models.FloatField(null=True, default=None)
    name = models.CharField(max_length=100,null=True, default=None)
    coach = models.CharField(max_length=100, null=True, default=None)

class Championship(models.Model):

    CHAMPIONSHIP_STATES = [
        ('in_progress', 'In Progress'),
        ('upcoming', 'Upcoming'),
        ('finished', 'Finished'),
    ]

    championship_name = models.CharField(max_length=100)
    year = models.IntegerField(null=True, default=None)
    start_date = models.DateField(null=True, default=None)
    end_date = models.DateField(null=True, default=None)
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='championship_winner')
    state = models.CharField(max_length=20, choices=CHAMPIONSHIP_STATES, default='upcoming')
    

class Ranking(models.Model): #Clasament
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    points = models.IntegerField(null=True, default=None)
    defeats = models.IntegerField(null=True, default=None)
    victories = models.IntegerField(null=True, default=None)
    draws = models.IntegerField(null=True, default=None)

    class Meta:
        unique_together = ('championship', 'team') 


class Match(models.Model):
    MATCH_STATES = [
        ('in_progress', 'In Progress'),
        ('upcoming', 'Upcoming'),
        ('finished', 'Finished'),
    ]

    final_score = models.CharField(max_length=10)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_team2')
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=MATCH_STATES, default='upcoming')
    date = models.DateField(null=True, default=None)