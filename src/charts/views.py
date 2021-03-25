from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


import requests
import json
import random
import time
import datetime
from charts.faceit_data import FaceitData

#from charts.faceit_api.faceit_data import FaceitData
User = get_user_model()

class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'homepage.html', {})

class StatsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'stats.html', {})        

class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about.html', {})

class SearchView(View):

    def get(self, request, format=None):
        faceit_data = FaceitData("FACEIT_API_KEY")
        if request.method == "GET":  # form submission
            query = request.GET.get("searchplayer")  # dict key, from html input
            get_player_details = faceit_data.player_details(query, 'csgo')

            if get_player_details == None:
                return render(request, 'base.html', {})

            else:
                get_player_id = get_player_details['player_id']
                api_url = "https://api.faceit.com/stats/api/v1/stats/time/users/{}/games/csgo?size=2000".format(get_player_id)
                res = requests.get(api_url).json()
                i = 0
                elo_history = []
                for match in res:     
                    elo_history.append(res[i].get("elo", None))
                    i += 1
                i = 0
                kd_history = []
                for match in res:     
                    kd_history.append(res[i].get("c2", None))
                    i += 1

                i = 0
                total_rounds = []
                for match in res:     
                    total_rounds.append(res[i].get("i12", None))
                    i += 1

                i = 0
                total_kills = []
                for match in res:     
                    total_kills.append(res[i].get("i6", None))
                    i += 1

                elo_history = list(filter(None, elo_history)) 
                elo_history.reverse()
                kd_history = list(filter(None, kd_history)) 
                kd_history.reverse()
                total_rounds = list(filter(None, total_rounds)) 
                total_rounds.reverse()
                total_kills = list(filter(None, total_kills)) 
                total_kills.reverse()


                matches = list(range(1, len(elo_history)))

                for i in range(0, len(elo_history)): 
                    elo_history[i] = int(elo_history[i])

                for i in range(0, len(total_rounds)): 
                    total_rounds[i] = int(total_rounds[i])

                for i in range(0, len(total_kills)): 
                    total_kills[i] = int(total_kills[i])

                #last 20
                api_url_last_20 = "https://api.faceit.com/stats/api/v1/stats/time/users/{}/games/csgo?size=20".format(get_player_id)
                res2 = requests.get(api_url_last_20).json()

                i = 0
                kd_history_last_20 = []
                for match in res2:     
                    kd_history_last_20.append(res2[i].get("c2", None))
                    i += 1

                i = 0
                total_kds_last_20 = []
                for match in res2:     
                    total_kds_last_20.append(res2[i].get("c2", None))
                    i += 1

                i = 0
                total_rounds_last_20 = []
                for match in res2:     
                    total_rounds_last_20.append(res2[i].get("i12", None))
                    i += 1

                i = 0
                total_kills_last_20 = []
                for match in res2:     
                    total_kills_last_20.append(res2[i].get("i6", None))
                    i += 1

                i = 0
                total_assists_last_20 = []
                for match in res2:     
                    total_assists_last_20.append(res2[i].get("i7", None))
                    i += 1

                i = 0
                total_kprs_last_20 = []
                for match in res2:     
                    total_kprs_last_20.append(res2[i].get("c3", None))
                    i += 1

                i = 0
                total_deaths_last_20 = []
                for match in res2:     
                    total_deaths_last_20.append(res2[i].get("i8", None))
                    i += 1

                i = 0
                total_maps_last_20 = []
                for match in res2:     
                    total_maps_last_20.append(res2[i].get("i1", None))
                    i += 1

                i = 0
                total_scores_last_20 = []
                for match in res2:     
                    total_scores_last_20.append(res2[i].get("i18", None))
                    i += 1

                i = 0
                total_match_results_last_20 = []
                for match in res2:     
                    total_match_results_last_20.append(res2[i].get("i10", None))
                    i += 1

                i = 0
                total_dates_last_20 = []
                for match in res2:     
                    total_dates_last_20.append(res2[i].get("date", None))
                    i += 1

                
                for i in range (len(total_match_results_last_20)):
                    if total_match_results_last_20[i]=='0':
                        total_match_results_last_20[i]='L'
                    else:
                        total_match_results_last_20[i]='W'

                current_time_unix_utc = datetime.datetime.utcnow().timestamp()
                
                i = 0
                total_time_ago_last_20 = []
                for timestamp in total_dates_last_20:
                    
                    total_dates_last_20[i] = str(datetime.timedelta(seconds=int(current_time_unix_utc) - (int(timestamp)/1000)))
                    i +=1

                kd_history_last_20 = list(filter(None, kd_history_last_20)) 
                kd_history_last_20.reverse()

                total_rounds_last_20 = list(filter(None, total_rounds_last_20))
                total_rounds_last_20.reverse()

                total_kills_last_20 = list(filter(None, total_kills_last_20)) 
                total_kills_last_20.reverse()

                for i in range(0, len(total_rounds_last_20)): 
                    total_rounds_last_20[i] = int(total_rounds_last_20[i])

                for i in range(0, len(total_kills_last_20)): 
                    total_kills_last_20[i] = int(total_kills_last_20[i])

                list_of_kprs_last_20 = [i / j for i, j in zip(total_kills_last_20, total_rounds_last_20)]
                sum_of_kprs_last_20 = sum(list_of_kprs_last_20)
                len_of_kprs_last_20 = len(list_of_kprs_last_20)
                KPR_last_20 = sum_of_kprs_last_20 / len_of_kprs_last_20
                KPR_last_20 = round(KPR_last_20, 2)

                list_of_kprs = [i / j for i, j in zip(total_kills, total_rounds)]
                sum_of_kprs = sum(list_of_kprs)
                len_of_kprs = len(list_of_kprs)
                KPR = sum_of_kprs / len_of_kprs
                KPR = round(KPR, 2)

                for i in range(0, len(kd_history_last_20)): 
                    kd_history_last_20[i] = float(kd_history_last_20[i])

                kd_history_last_20 = round((sum(kd_history_last_20) / len(kd_history_last_20)), 2)

                labels = matches
                default_items = elo_history

                statistics = faceit_data.player_stats(get_player_id, 'csgo')
                lifetime_kd = statistics['lifetime']['Average K/D Ratio']
                current_elo = get_player_details['games']['csgo']['faceit_elo']
                skill_level = get_player_details['games']['csgo']['skill_level']

                faceit_levels = {
                1:"/static/img/faceit1.svg",
                2:"/static/img/faceit2.svg",
                3:"/static/img/faceit3.svg",
                4:"/static/img/faceit4.svg",
                5:"/static/img/faceit5.svg",
                6:"/static/img/faceit6.svg",
                7:"/static/img/faceit7.svg",
                8:"/static/img/faceit8.svg",
                9:"/static/img/faceit9.svg",
                10:"/static/img/faceit10.svg",
                } 
                current_skill_level = faceit_levels[skill_level]

                faceit_progression = {
                1:"800",
                2:"950",
                3:"1100",
                4:"1250",
                5:"1400",
                6:"1550",
                7:"1700",
                8:"1850",
                9:"2000",
                10:"2001",
                } 
                current_progress = faceit_progression[skill_level]

                data = {
                        "kd_history": kd_history,
                        "matches": matches,
                        "labels": labels,
                        "default": default_items,
                        "lifetime_kd": lifetime_kd,
                        "current_elo": current_elo,
                        "get_player_id": get_player_details,
                        "skill_level": skill_level,
                        "current_skill_level": current_skill_level,
                        "KPR":KPR,
                        "kd_history_last_20":kd_history_last_20,
                        "KPR_last_20":KPR_last_20,
                        "current_progress": current_progress,
                        "total_kills_last_20": total_kills_last_20,
                        "total_assists_last_20":total_assists_last_20,
                        "total_kprs_last_20":total_kprs_last_20,
                        "total_deaths_last_20":total_deaths_last_20,
                        "total_scores_last_20":total_scores_last_20,
                        "total_match_results_last_20":total_match_results_last_20,
                        "total_dates_last_20": total_dates_last_20,
                        "total_maps_last_20":total_maps_last_20,
                        "total_kds_last_20":total_kds_last_20,        
                }
                return render(request, 'stats.html', { "data": data })