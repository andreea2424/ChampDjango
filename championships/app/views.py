from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Team, Championship, Ranking, Match
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils import timezone
import json

@csrf_exempt
def create_team(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        team = Team.objects.create(**data)
        return JsonResponse({'message': 'Team created successfully', 'team_id': team.id})
    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def create_ranking(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        championship_id = data.get('championship')
        championship = Championship.objects.get(id=championship_id)
        data['championship'] = championship

        team_id = data.get('team')
        team = Team.objects.get(id=team_id)
        data['team'] = team

        ranking = Ranking.objects.create(**data)
        return JsonResponse({'message': 'Ranking created successfully', 'ranking_id': ranking.id})
    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def create_championship(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        
        winner_id = data.get('winner')
        winner_team = Team.objects.get(id=winner_id)
        data['winner'] = winner_team

        championship = Championship.objects.create(**data)
        return JsonResponse({'message': 'Championship created successfully', 'championship_id': championship.id})
    
    return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def create_match(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        team = Team.objects.create(**data)
        return JsonResponse({'message': 'Team created successfully', 'team_id': team.id})
    return JsonResponse({'error': 'Invalid request method'})

def get_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    return JsonResponse({'id': team.id, 'name': team.name, 'coach': team.coach, 'match_count': team.match_count})



@csrf_exempt
def create_match2(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print("#######")
        print(data['team1_id'])

        # Assuming your request contains team1_id, team2_id, championship_id, date, and other necessary fields
        team1 = Team.objects.get(pk=data['team1_id'])
        team2 = Team.objects.get(pk=data['team2_id'])
        championship = Championship.objects.get(pk=data['championship_id'])
        current_date = timezone.now().date()
        match_date = timezone.datetime.strptime(data['date'], '%Y-%m-%d').date()

        if match_date < current_date:
            state = 'finished'
        elif match_date == current_date:
            state = 'in_progress'
        else:
            state = 'upcoming'

        # Create the match
        match = Match.objects.create(
            final_score=data['final_score'],
            team1=team1,
            team2=team2,
            championship=championship,
            state=state,
            date=data['date']
        )

        return JsonResponse({'message': 'Match created successfully', 'match_id': match.id})

    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def start_match(request, match_id):
    if request.method == 'POST':
        try:
            match = Match.objects.get(pk=match_id)
        except Match.DoesNotExist:
            return JsonResponse({'error': 'Match not found'}, status=404)
        match = Match.objects.get(id=match_id)
        if (match.state == 'upcoming'):
            match.state = 'in_progress'
            match.save()
        else:
            return JsonResponse({'error': 'The match state cannot be changed. It is not in the upcoming state.'}, status=400)
    return JsonResponse({'message': 'Match started successfully'})

@csrf_exempt
def generate_upcoming_matches(championship):

    teams = Team.objects.all()
    team_count = len(teams)

    if team_count >= 2:
        for i in range(team_count - 1):
            for j in range(i + 1, team_count):
                Match.objects.create(
                    team1=teams[i],
                    team2=teams[j],
                    championship=championship,
                    date=championship.start_date,
                    state='upcoming'
                )

@csrf_exempt
def start_championship(request, championship_id):
    if request.method == 'POST':
        try:
            championship = Championship.objects.get(pk=championship_id)
        except Championship.DoesNotExist:
            return JsonResponse({'error': 'Championship not found'}, status=404)
        championship = Championship.objects.get(id=championship_id)
        if (championship.state == 'upcoming'):
            championship.state = 'in_progress'
            championship.save()
            generate_upcoming_matches(championship)
        else:
            return JsonResponse({'error': 'The championship state cannot be changed. It is not in the upcoming state.'}, status=400)
    return JsonResponse({'message': 'Championship started successfully'})