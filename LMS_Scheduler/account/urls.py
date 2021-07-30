from django.urls import path
from django.urls.resolvers import URLPattern
from .import views

from django.contrib import admin
import lms.views

urlpatterns = [
    path('signup/', views.signup , name = 'signup'),
    path('login/',views.manuallogin,name="manuallogin"),

    path('kakaologin/', views.kakoredirect, name="kakaologin"),
    path('login/kakao_login', views.kakao_login , name = 'kakao_login'),
    path('signup/kakao', views.kakao_signup, name="kakao_signup"),
    path('oauth/', views.oauth, name="oauth"),
    
    path('signup/LMSsignup',views.idSignup,name="idSignup"),
    path('signup/lmsSignup',views.lmsSignup,name="lmsSignup"),
    path('signup/IDSignup',views.idsignuppage,name="idsignuppage"),
    path('calendar/', views.calendar, name = "calendar"),
    path('calendar/customize', views.customize, name = "customize"),
    path('home/', lms.views.home, name = "home"),
    path('mainLogin',views.mainLogin, name = "mainlogin"),
    path('statistic/', views.statistic, name = "statistic"),
    path('mypage/',views.mypage,name="mypage"),
    path('',views.logout,name="logout"), # 초기화면 때문에 include 처리 안함
    path('ranking/', views.ranking, name = "ranking"),

    path('usertype', views.usertype, name = "usertype"),
    path('mypage/create',views.create,name ="create"),
    path('mypage/edit', views.edit, name = "edit"),
    path('qnaAnswer/',views.qnaAnswer,name ="qnaAnswer"),
    path('calendar/checkin', views.checkin, name = "checkin"),
]