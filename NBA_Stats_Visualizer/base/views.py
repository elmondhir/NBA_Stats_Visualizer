from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from nba_api.stats.endpoints import TeamGameLog, BoxScoreAdvancedV2
# Create your views here.
import json

def home(request):
    if request.method == 'POST':
        # Assuming you named your form fields 'statType' and 'shortText'
        stat_type = request.POST.get('statType')
        short_text = request.POST.get('shortText')

        from collections import defaultdict
        

        teams_game_stats = {}
        for team_id in [1610612752]:
            cumulative_off_rating = 0
            cumulative_def_rating = 0

            game_stats =  []
            games = TeamGameLog(team_id=team_id, season="2023", season_type_all_star="Regular Season").get_dict()['resultSets'][0]["rowSet"]
            for game in games:
                game_id = game[1]

                boxscore = BoxScoreAdvancedV2(game_id=game_id).get_dict()['resultSets'][1]["rowSet"]
                for index, tm in enumerate(boxscore):
                    if tm[1] == 1610612752:
                        OFF_RATING = boxscore[index][9]
                        DEF_RATING = boxscore[index][7]

                        
                        cumulative_off_rating += OFF_RATING
                        cumulative_def_rating += DEF_RATING
                        
                        average_off_rating = (cumulative_off_rating / (len(game_stats)+1)) if len(game_stats) > 0 else OFF_RATING
                        average_def_rating = (cumulative_def_rating / (len(game_stats)+1)) if len(game_stats) > 0 else DEF_RATING

                        
                        game_stats.append(
                            {"Game_id": game_id,
                            'OFF_RATING': OFF_RATING,
                            'DEF_RATING': DEF_RATING,
                            'Average_OFF_RATING': average_off_rating,
                            'Average_DEF_RATING': average_def_rating,
                            }
                            )
                        
            teams_game_stats[team_id] = game_stats
        # team_id = 1610612744 #GSW 1610612752 # Knicks

        return render(request, 'home.html', context={"game_stats":teams_game_stats})

    
    return render(request, 'home.html')#
