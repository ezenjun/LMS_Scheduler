from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from .models import *
from django.http import JsonResponse  
import requests
import json
# Create your views here.

def kakao_signup(request):
    login_request_uri = 'https://kauth.kakao.com/oauth/authorize?'
    client_id = 'f73eac580e0bc9a9152e0eaedda3100a'
    redirect_uri = 'http://127.0.0.1:8000/oauth'

    login_request_uri += 'client_id=' + client_id
    login_request_uri += '&redirect_uri=' + redirect_uri
    login_request_uri += '&response_type=code'
    
    return redirect(login_request_uri)

def oauth(request):
    authcode = request.GET['code']
    kakao = 'https://kauth.kakao.com/oauth/token'
    data = dict(
        grant_type='authorization_code',
        client_id='f73eac580e0bc9a9152e0eaedda3100a',
        redirect_uri ='http://127.0.0.1:8000/oauth',
        code = authcode,
    )
    response = requests.post('https://kauth.kakao.com/oauth/token', data=data)
    if response.status_code == 200:
        token = response.json().get('access_token')
        user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization':f'Bearer {token}'})
        text = json.loads(user_info_response.text)
        kakaoId = text['id']
        if User.objects.filter(username=kakaoId).exists():
            return render(request,'mainLogin.html',{'error':"이미 존재하는 사용자입니다."})
        else: 
            user=User.objects.create_user(
                kakaoId
            )
            auth.login(request,user)
        return render(request, 'lmsInfo.html')

def kakoredirect(request):
    authcode = request.GET['code']
    kakao = 'https://kauth.kakao.com/oauth/token'
    data = dict(
        grant_type='authorization_code',
        client_id='f73eac580e0bc9a9152e0eaedda3100a',
        redirect_uri ='http://127.0.0.1:8000/kakaologin',
        code = authcode,
    )
    response = requests.post('https://kauth.kakao.com/oauth/token', data=data)
    if response.status_code == 200:
        token = response.json().get('access_token')
        user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization':f'Bearer {token}'})
        text = json.loads(user_info_response.text)
        kakaoId = text['id']
        if User.objects.filter(username=kakaoId).exists():
            auth.login(request, request.user)
            return render(request, 'home.html')        

def kakao_login(request):
    login_request_uri = 'https://kauth.kakao.com/oauth/authorize?'
    client_id = 'f73eac580e0bc9a9152e0eaedda3100a'
    redirect_uri = 'http://127.0.0.1:8000/kakaologin'

    login_request_uri += 'client_id=' + client_id
    login_request_uri += '&redirect_uri=' + redirect_uri
    login_request_uri += '&response_type=code'
    
    return redirect(login_request_uri)



def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/home')
        else:
            return render(request,'mainLogin.html',{'error':"사용자 이름 혹은 패스워드가 일치하지 않습니다"})
    else:
        return render(request,'mainLogin.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


def signup(request):
    return render(request,'signup.html')

def idsignuppage(request):
    return render(request, 'idSignup.html')

def idSignup(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request,'idSignup.html',{'error':"이미 존재하는 사용자입니다."})
        if password==request.POST['passwordCheck']:
            user=User.objects.create_user(
                username,password=password
            )
            auth.login(request,user)
            return render(request,'lmsInfo.html')
        else :
            return render(request,'idSignup.html',{'error':"비밀번호 확인이 일치하지 않습니다"})
    else:
        return render(request,'idSignup.html')

def lmsSignup(request):
    if request.method=="POST":
        user = request.user
        lmsId=request.POST['lmsId']
        lmsPwd=request.POST['lmsPwd']
        if lmsPwd==request.POST['lmsPwdCheck']:
            customer = Customer(user=user, lmsId = lmsId, lmsPwd=lmsPwd)
            customer.save()
            return render(request,'home.html')
        else :
            return render(request,'lmsInfo.html',{'error':"비밀번호 확인이 일치하지 않습니다"})
    else:
        return render(request,'lmsInfo.html')



def manuallogin(request):
    return render(request,'idLogin.html')