from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .models import Luckydraw, Participants, Winner
from django.contrib import messages
from django.http import HttpResponse
import json
import facebook
import random

def login(request):
  return render(request, 'luckywinner/login.html')

def index(request):
  return render(request, 'luckywinner/index.html')

@login_required
def home(request):
  user = User.objects.get(username=request.user.username)
  if Luckydraw.objects.filter(status=True).exists():
    luckydraw = Luckydraw.objects.get(status=True)
    print(luckydraw.image)
  else:
    luckydraw = None

  if request.user.is_superuser:
    params = {'luckydraw':luckydraw}
    return render(request, 'luckywinner/home.html', params)
  
  # Facebook authenticated USer
  else:
    page_list = []
    auth = user.social_auth.first()
    token = auth.extra_data['access_token']
    graph = facebook.GraphAPI(token)
    fields = ['id,name,email,gender,birthday,link']
    profile = graph.get_object('me', fields=fields)
    # print(profile)
    facebook_id = profile["id"]
    # Checking if participants already existed
    if Participants.objects.filter(facebook_id=facebook_id).exists():
      participant = Participants.objects.get(facebook_id=facebook_id)
      profile = graph.get_object('me/likes/748066388700226/')
      likes = profile["data"]
      if len(likes)>0:
        messages.info(request, "You have already Participated. Please visit our facebook page to stay updated ")
      else:
        participant.status = False
        messages.info(request, "Please like our facebook page to participate")

    # If participant doesn't existed
    else:
      try:
        name = profile["name"]
      except:
        name = ''
      try:
        gender = profile["gender"]
      except:
        gender = ''
      try:
        birthday = profile["birthday"]
      except:
        birthday = ''
      try:
        link = profile["link"]
      except:
        link = ''
      try:
        facebook_id = profile['id']
      except:
        facebook_id = ''
      try:
        email = profile['email']
      except:
        email = ''
      participant = Participants(facebook_id=facebook_id, name=name, email=email, gender=gender, birthday=birthday, link=link)
      participant.save()
      messages.info(request, "Note: You have to like our facebook page to participate")

    #print(json.dumps(profile, indent=4))

    params = {'luckydraw':luckydraw, 'participant':participant}
    return render(request, 'luckywinner/home.html', params)

# @login_required
# def home(request):
#   user = User.objects.get(username=request.user.username)
#   auth = user.social_auth.first()
#   token = auth.extra_data['access_token']
#   graph = facebook.GraphAPI(token)
#   #fields = ['me/likes/748066388700226/']
#   profile = graph.get_object('me/likes/748066388700226/')
#   likes = profile["data"]
#   print(likes)
#   print(len(likes))
#   return HttpResponse('Hello')


@login_required
def participate(request, name):
  if request.user.is_superuser:
    return render(request, 'luckywinner/home.html')
  else:
    user = User.objects.get(username=request.user.username)
    if Luckydraw.objects.filter(status=True).exists():
      luckydraw = Luckydraw.objects.get(status=True)
      print(luckydraw.image)
    else:
      luckydraw = None

    auth = user.social_auth.first()
    token = auth.extra_data['access_token']
    graph = facebook.GraphAPI(token)
    fields = ['id']
    profile = graph.get_object('me/likes/748066388700226/')
    fb_id = graph.get_object('me', fields=fields)
    likes = profile["data"]
    facebook_id = fb_id["id"]

    if len(likes)>0:
      participant = Participants.objects.get(facebook_id=facebook_id)
      lucky = Luckydraw.objects.get(name=name)
      if participant.status==False:
        participant.status = True
        participant.luckydraw = lucky
        participant.save()
        messages.info(request,"Thank you for participating. Please visit our facebook page to stay updated.")
      else:
        messages.info(request,"You have already Participated. Please visit our facebook page to stay updated. ")

    else:
      participant = Participants.objects.get(facebook_id=facebook_id)
      participant.status = False
      participant.save()
      messages.info(request,"Please Like our facebook page to participate")
    params = {'luckydraw':luckydraw, 'participant':participant}
    return render(request, 'luckywinner/home.html', params)

@login_required
def winner_select(request):
  return render(request, 'luckywinner/winner_select.html')

@login_required
def currentwinner(request):
  luckydraw = Luckydraw.objects.get(status=True)
  participant = Participants.objects.filter(status=True, luckydraw=luckydraw)
  num_of_participant = len(participant)
  random_num = random.randint(1, num_of_participant)
  print(random_num)
  winner = participant[random_num-1]
  winner_list = Winner.objects.all()
  for i in winner_list:
    if i == winner:
      random_num = random.randint(1, num_of_participant)
      winner = participant[random_num-1]
    else:
      break
  new_winner = Winner(name=winner, luckydraw=luckydraw)
  new_winner.save()
  params = {'winner':winner}
  return render(request, 'luckywinner/winner.html', params)

@login_required
def overallwinner(request):
  participant = Participants.objects.filter(status=True)
  num_of_participant = len(participant)
  random_num = random.randint(1, num_of_participant)
  print(random_num)
  winner = participant[random_num-1]
  luckydraw = Luckydraw.objects.get(name = winner.luckydraw)
  new_winner = Winner(name=winner, luckydraw=luckydraw)
  new_winner.save()
  params = {'winner':winner}
  return render(request, 'luckywinner/winner.html', params)

def privacy(request):
  return render(request, 'luckywinner/privacy.html')