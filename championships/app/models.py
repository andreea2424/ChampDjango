# models.py

from django.db import models

class Team(models.Model):
    match_count = models.IntegerField(null=True, default=None)
    establishment_year = models.IntegerField(null=True, default=None)
    total_rating = models.FloatField(null=True, default=None)
    name = models.CharField(max_length=100,null=True, default=None)
    coach = models.CharField(max_length=100, null=True, default=None)

class Championship(models.Model):
    year = models.IntegerField(null=True, default=None)
    start_date = models.DateField(null=True, default=None)
    end_date = models.DateField(null=True, default=None)
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='championship_winner')
    championship_name = models.CharField(max_length=100)

class Standings(models.Model):
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    points = models.IntegerField(null=True, default=None)
    defeats = models.IntegerField(null=True, default=None)
    victories = models.IntegerField(null=True, default=None)
    draws = models.IntegerField(null=True, default=None)

    class Meta:
        unique_together = ('championship', 'team')  # Ensure no duplicates for a championship and a team

class Match(models.Model):
    final_score = models.CharField(max_length=10)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_team2')
    championship_id = models.ForeignKey(Championship, on_delete=models.CASCADE)
