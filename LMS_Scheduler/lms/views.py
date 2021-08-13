from django.shortcuts import redirect, render
from bs4 import BeautifulSoup
import requests
from django.contrib.auth.models import AnonymousUser, User
from account.models import *
from datetime import datetime
import time
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def finish(request):
    return render(request,"home.html")
    
def home(request):
    #세션만들기
    session=requests.session()
    #로그인 하는 페이지의 general-requestURL에서 url 가져옴
    url="https://lms.kau.ac.kr/login/index.php"
        
    #가져오고 싶은 데이터 (form data)
    data={
        "username":Customer.objects.get(user = request.user).lmsId,
        "password":Customer.objects.get(user = request.user).lmsPwd  
    }
    response=session.post(url, data=data ) #요청을 모방하면됨 (get, post, put 등)
        
    #로그인 실행
    response.raise_for_status()
        
        
    #LMS 접근
    url="http://lms.kau.ac.kr/local/ubion/user/?year=2021&semester=10"
    response=session.get(url)
    response.raise_for_status()

    #Crawling 시작 
    soup=BeautifulSoup(response.text,"html.parser")
    print(soup)
    #강의명 긁어오기+
    courselist = soup.find("tbody", {"class": "my-course-lists"})
    courses = courselist.find_all('a')
    print("강의 리스트")
    if(Class.objects.filter(user=request.user).exists()==False):
        i=0
        for course in courses:
            i=i+1
            userclass = Class(user=request.user, class_name = course.get_text(),rank=i)
            userclass.save()
            print("db 저장용 ", userclass.class_name)

    print("------------------------------------")
    
    # 강의 세부페이지 링크 긁어오기
    id = 0
    lectures = []
    for link in courselist.find_all('a'):
        id += 1
        if(id==5):continue
        # print("id : ", id)
        url = link.get('href') #링크 긁어오기
        response=session.get(url)   #링크로 넘어가기
        response.raise_for_status()
        soup=BeautifulSoup(response.text,"html.parser")
        course = soup.find("div", {"class": "total_sections"})  #전체
        firstweek = course.find("li", {"id": "section-5"})
        section = firstweek.find("ul", {"class": "section img-text"}) 
        if section != None:
            #li class activity assign modtype_assign (과제)
            lecture = {}
            if section.find("li", {"class": "assign"}) != None:
                instance = section.find('li',class_="assign")
                assignment_name = instance.find("span", {"class": "instancename"})
                assignment_link = instance.find('a').get('href')
                # print("과제명 : ", assignment_name.get_text())
                # print("과제링크 : ", assignment_link)
                response=session.get(assignment_link)   #링크로 넘어가기
                response.raise_for_status()
                soup=BeautifulSoup(response.text,"html.parser")
                submissionstatus = soup.find("div", {"class": "submissionstatustable"})
                alltr = submissionstatus.find_all("tr")
                try:
                    duedate = alltr[2].find("td", {"class": "cell c1 lastcol"})
                except:
                    duedate = "no duedate"
                # print("duedate : ", duedate.get_text())
                # assignment = {'assignment_name' : assignment_name.get_text(), 'assignment_link' : assignment_link, 'assignment_duedate' : duedate.get_text()}
                # lecture.append(assignment)
                lecture["assignment_name"] = assignment_name.get_text()
                lecture["assignment_link"] = assignment_link
                lecture["assignment_duedate"] = duedate

            #li class activity vod modtype_vod (강의VOD)
            if section.find("li", {"class": "vod"}) != None:
                instance = section.find("li", {"class": "vod"})
                vod_name = instance.find("span", {"class": "instancename"})
                vod_link = instance.find('a').get('onclick')
                vod_duedate = instance.find("span", {"class":"text-ubstrap"})
                # print("vod 명 : ",vod_name.get_text())
                # print("vod 링크 : ",vod_link)
                # print("duedate : ",vod_duedate.get_text())
                # vod = {'vod' : vod_name.get_text(), 'vod_link' : vod_link, 'vod_duedate': vod_duedate.get_text()}
                lecture["vod"] = vod_name.get_text()
                lecture["vod_link"] = vod_link
                lecture["vod_duedate"] = vod_duedate.get_text()
                # lecture.append(vod)

            #li class activity url modtype_url (강의 link)
            if section.find("li", {"class": "url"}) != None:
                instance = section.find("li", {"class": "url"})
                link_name = instance.find("span", {"class": "instancename"})
                url_link = instance.find('a').get('onclick')
                # print("강의 명 : ", link_name.get_text())
                # print("강의 링크 : ",url_link)
                # url = {'link_name': link_name.get_text(), 'url_link': url_link}
                lecture["link_name"] = link_name.get_text()
                lecture["url_link"] = url_link
                # lecture.append(url)


            #li class activity quiz modtype_quiz (퀴즈)
            if section.find("li", {"class": "quiz"}) != None:
                instance = section.find("li", {"class": "quiz"})
                quiz_name = instance.find("span", {"class": "instancename"})
                # print("퀴즈 명 : ",quiz_name.get_text())
                # quiz = {'quiz_name' : quiz_name.get_text()}
                lecture['quiz_name'] = quiz_name.get_text()
                if instance.find('a') != None:
                    quiz_link = instance.find('a').get('href')
                    # print("퀴즈 링크 : ",quiz_link)
                    lecture['quiz_link'] = quiz_link
                else:
                    print("no link")
                    lecture['quiz_link'] = 'no link'
                # lecture.append(quiz)
        else:
            print("No Assginment / Lecture / Quiz")
            lecture = {}
        print(lecture)
        each_lecture = {'id' : id, 'body' : lecture}
        lectures.append(each_lecture)
        print("------------------------------------")

    print(lectures)
    cur_user = request.user
    print("curuser:", cur_user)
    # if cur_user is None:
    #     return render(request, "mainLogin.html")
    # if cur_user.is_authenticated:
    #     user = User.objects.get(user = request.user)
    #     return render(request, "home.html")
    # else:
    #     return render(request, "mainLogin.html")
    if cur_user.is_anonymous:
        print('aaa')
        return redirect('mainLogin')
    else:
     return render(request, 'home.html', {'userlectures' : lectures})

@csrf_exempt
def test(request):
    if request.is_ajax():
        #do something
        request_data = json.loads(request.body)
        dailytime = request_data['time']
        print(dailytime)
        #dailytime = time.strftime('%H:%M:%S', time.gmtime(request_data['time']))

        try:
            id = Statistics.objects.filter(user = request.user)
            date = Statistics.objects.filter(date = datetime.now())
            curexits = Statistics.objects.get(user = request.user, date = datetime.now())
        except Statistics.DoesNotExist:
            id = None
            date = None
            curexits = None
        print(curexits)
        if id != None:
            if date != None : #오늘 날짜 존재
                curexits.daily += dailytime
                curexits.save()
            else: #오늘 날짜 미존재
                Statistic = Statistics(user=request.user, daily = dailytime, date = datetime.now())
                Statistic.save()
        else:
            Statistic = Statistics(user=request.user, daily = dailytime, date = datetime.now())
            Statistic.save()
        
        return render(request, 'home.html')
    else:
     return render(request, 'home.html')