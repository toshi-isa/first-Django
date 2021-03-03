from apiclient.discovery import build
import datetime
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import C_id
from .models import Comment
from .forms import CommentForm
 

C_ids = C_id.objects.all()
kazu = len(C_ids)
zesyukei= []


def channnel(yid):
  key = "AIzaSyA2hFWKYk8zCwTYxOPq145RrVrV5o0v3lQ"
  name = "youtube"
  ver = "v3"
  youtube = build( name , ver , developerKey = key)
  respons = youtube.channels().list (part="id,snippet,statistics" , id = yid).execute()["items"]
  dtm = respons[0]["snippet"]["publishedAt"]
  if len(dtm)==20:
    hdtm = datetime.datetime.strptime(dtm,"%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
  else:
    hdtm = datetime.datetime.strptime(dtm,"%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
  url = respons[0]["snippet"]["thumbnails"]["medium"]["url"]
  name = respons[0]['snippet']["title"]
  sosaisei = int(respons[0]["statistics"]["viewCount"])
  torokuday = int(respons[0]["statistics"]["subscriberCount"])
  kosyukei = [ url , name , hdtm , sosaisei , torokuday]
  
  if len(zesyukei) == kazu:
    zesyukei.clear()

  zesyukei.append(kosyukei)
 

def index(request):

  comments = Comment.objects.all()
  commentForm = CommentForm()

  for yid in C_ids:
    channnel(yid)


  context ={
    "comments" : comments,
    "commentForm" : commentForm,
    "zesyukei" : zesyukei,
   }  

  return render(request,"bbs/index.html",context)

def create(request):

  if request.method == "POST":
    commentForm = CommentForm(request.POST)
    if commentForm.is_valid():
      comments = commentForm.save()

  comments = Comment.objects.all()

  context = {
   "C_ids" : C_ids,
    "comments" : comments,
    "commentForm" : commentForm,
    "zesyukei" : zesyukei,
   }
  
  return render(request, "bbs/index.html",context)