from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from nba_api.stats.endpoints import TeamGameLog, BoxScoreAdvancedV2
from nba_api.stats.static import teams
from datetime import datetime
# Create your views here.
import json

def home(request):
    if request.method == 'POST':
        # Assuming you named your form fields 'statType' and 'shortText'
        # stat_type = request.POST.get('statType')
        selected_options = request.POST.getlist('selected_options')
        from_date = request.POST.get('fromDate')
        to_date = request.POST.get('toDate')        

        print(selected_options)

        teams_dict = teams.get_teams()
        teams_abb = [team["abbreviation"] for team in teams_dict if team["abbreviation"] in selected_options] # or use abbreviation
        teams_ids= [team["id"] for team in teams_dict if team["abbreviation"] in selected_options]
        
        teams_game_stats = {}
        for team_id, team_abb in zip(teams_ids, teams_abb):
            cumulative_off_rating = 0
            cumulative_def_rating = 0

            game_stats =  []
            games = TeamGameLog(team_id=team_id, season="2023", season_type_all_star="Regular Season",
                                date_from_nullable=datetime.strptime(from_date, "%Y-%m-%d").strftime("%m/%d/%Y"),
                                date_to_nullable= datetime.strptime(to_date, "%Y-%m-%d").strftime("%m/%d/%Y"), 
                                ).get_dict()['resultSets'][0]["rowSet"]
            
            
            for game in games:
                game_id = game[1]

                boxscore = BoxScoreAdvancedV2(game_id=game_id).get_dict()['resultSets'][1]["rowSet"]
                for index, tm in enumerate(boxscore):
                    if tm[1] == team_id:
                        OFF_RATING = boxscore[index][9]
                        DEF_RATING = boxscore[index][7]

                        
                        cumulative_off_rating += OFF_RATING
                        cumulative_def_rating += DEF_RATING
                        
                        average_off_rating = (cumulative_off_rating / (len(game_stats)+1)) if len(game_stats) > 0 else OFF_RATING
                        average_def_rating = (cumulative_def_rating / (len(game_stats)+1)) if len(game_stats) > 0 else DEF_RATING

                        
                        game_stats.append(
                            {"team_abv": team_abb,
                            "Game_id": game_id,
                            'OFF_RATING': OFF_RATING,
                            'DEF_RATING': DEF_RATING,
                            'Average_OFF_RATING': average_off_rating,
                            'Average_DEF_RATING': average_def_rating,
                            }
                            )
                        
            teams_game_stats[team_id] = game_stats

        return render(request, 'home.html', context={"game_stats":teams_game_stats})

    team_dict = teams.get_teams()
    team_list = [team["abbreviation"] for team in team_dict] # or use abbreviation
    
    return render(request, 'home.html', context={"team_list": team_list})#
