from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import auth
from django.utils import timezone
from .models import *
from django.http import JsonResponse  
import requests
import json
from lms.views import home
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def kakao_signup(request):
    login_request_uri = 'https://kauth.kakao.com/oauth/authorize?'
    client_id = 'f73eac580e0bc9a9152e0eaedda3100a'
    redirect_uri = 'http://127.0.0.1:8000/account/oauth'

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
        redirect_uri ='http://127.0.0.1:8000/account/oauth',
        code = authcode,
    )
    response = requests.post('https://kauth.kakao.com/oauth/token', data=data)
    if response.status_code == 200:
        token = response.json().get('access_token')
        user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization':f'Bearer {token}'})
        text = json.loads(user_info_response.text)
        kakaoId = "kakao"+str(text['id'])
        if User.objects.filter(username=kakaoId).exists():
            return redirect(mainLogin)
        else: 
            user=User.objects.create_user(
                kakaoId, password='0'
            )
            auth.login(request,user)
        return redirect(lmsSignup)

def kakao_login(request):
    login_request_uri = 'https://kauth.kakao.com/oauth/authorize?'
    client_id = 'f73eac580e0bc9a9152e0eaedda3100a'
    redirect_uri = 'http://127.0.0.1:8000/account/kakaologin'

    login_request_uri += 'client_id=' + client_id
    login_request_uri += '&redirect_uri=' + redirect_uri
    login_request_uri += '&response_type=code'
    
    return redirect(login_request_uri)

def kakoredirect(request):
    authcode = request.GET['code']
    kakao = 'https://kauth.kakao.com/oauth/token'
    data = dict(
        grant_type='authorization_code',
        client_id='f73eac580e0bc9a9152e0eaedda3100a',
        redirect_uri ='http://127.0.0.1:8000/account/kakaologin',
        code = authcode,
    )
    response = requests.post('https://kauth.kakao.com/oauth/token', data=data)
    if response.status_code == 200:
        token = response.json().get('access_token')
        user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={'Authorization':f'Bearer {token}'})
        text = json.loads(user_info_response.text)
        kakaoId = "kakao"+str(text['id'])
        user=auth.authenticate(request,username=kakaoId,password='0')
        print("user - ", user)
        if User.objects.filter(username=kakaoId).exists():
            auth.login(request, user)
            return redirect(home)    


def mainLogin(request):
    return render(request, "mainLogin.html")

def logout(request):
    auth.logout(request)
    print("logout success")
    return redirect('mainLogin')


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
            return redirect('lmsSignup')
        else :
            return render(request,'idSignup.html',{'error':"비밀번호 확인이 일치하지 않습니다"})
    else:
        return render(request,'idSignup.html')
#lmssignup과 lmsinfo는 동일한 기능을 하는 이름
def lmsSignup(request): 
    if request.method=="POST":
        user = request.user
        lmsId=request.POST['lmsId']
        lmsPwd=request.POST['lmsPwd']
        if lmsPwd==request.POST['lmsPwdCheck']:
            customer = Customer(user=user, lmsId = lmsId, lmsPwd=lmsPwd, name='name', color='#eee', stamp='1', calendarDaystart='0', font = '1', basic='1',language='1')
            customer.save()
            return redirect(home)
        else :
            return render(request,'lmsInfo.html',{'error':"비밀번호 확인이 일치하지 않습니다"})
    else:
        return render(request,'lmsInfo.html')
#초기로그인
def manuallogin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(request,username=username,password=password)
        if user != None:
            auth.login(request,user)
            return redirect(home)
        else:
            return render(request,'idLogin.html',{'error':"사용자 이름 혹은 패스워드가 일치하지 않습니다"})
    else:
        return render(request,'idLogin.html')

def calendar(request):
    return render(request,'calendar.html')


def mypage(request):
    user = Customer.objects.get(user = request.user)
    myid = str(user.user)
    qnas = Qna.objects
    if len(Qna.objects.filter(user = request.user)) !=0:
        myqnas= Qna.objects.filter(user = request.user)
        print(myqnas)
    else:
        myqnas = None
        print(myqnas)
    
    notices = Notices.objects
    return render(request,'mypage.html', {'user':user, 'qnas':qnas,'myqnas':myqnas, 'notices':notices, 'myid':myid})

def customize(request):
    return render(request, 'customize.html')

def statistic(request):
    return render(request, "statistic.html")

def ranking(request):
    return  render(request, "ranking.html")
    
def new(request):
    return render(request,'new.html')

# def create(request):
#     faq=Faq()
#     faq.user=request.POST.get('user')
#     faq.title=request.POST.get('faq_title')
#     faq.body=request.POST.get('faq_body')
#     faq.save()
#     return redirect(home)


@csrf_exempt
def usertype(request):
    if request.is_ajax():
        #do something
        request_data = json.loads(request.body)
        inputtype = request_data['usertype']
        print(inputtype)
        #dailytime = time.strftime('%H:%M:%S', time.gmtime(request_data['time']))

        try:
            curexits = Priority.objects.get(user = request.user)
            print('try', curexits)
        except Priority.DoesNotExist:
            curexits = None
            print('execp', curexits)
            

        print('test', curexits)    
        if curexits != None:
            curexits.usertype = inputtype
            curexits.save() 
        else:
            newPriority = Priority(user=request.user, usertype = inputtype)
            newPriority.save()
        
        return render(request, 'mypage.html')
    else:
     return render(request, 'mypage.html')

def create(request):
    qna=Qna()
    print(request.GET['title'])
    qna.user = request.user
    qna.qna_title=request.GET['title']
    qna.qna_body=request.GET['body']
    qna.qna_date=timezone.datetime.now()
    qna.qna_answer = ""
    qna.qna_view = 0
    qna.save()
    return redirect('mypage')

def edit(request):
    user=request.user
    lmsuser = Customer.objects.get(user = request.user)

    password=request.POST['userpwd']
    pwdcheck = request.POST['userpwdchk']
    lmsPwd = request.POST['lmsPwd']
    lmsPwdchk = request.POST['lmsPwdchk']

    if password == pwdcheck & lmsPwd == lmsPwdchk:
        user.password=request.POST['userpwd']
        lmsuser.lmsId = request.POST['lmsId']
        lmsuser.lmsPwd = request.POST['lmsPwd']
        user.save()
        lmsuser.save()
    
    
    return redirect('mypage')

def qnaAnswer(request):

    return render(request,'qnaAnswer.html')