from django.urls import path
from django.urls.resolvers import URLPattern
from .import views

from django.contrib import admin
import lms.views

urlpatterns = [
    path('signup/', views.signup , name = 'signup'),
    path('login/kakao_login', views.kakao_login , name = 'kakao_login'),
    path('login/',views.manuallogin,name="manuallogin"),
    path('signup/kakao', views.kakao_signup, name="kakao_signup"),
    path('signup/LMSsignup',views.idSignup,name="idSignup"),
    path('signup/lmsSignup',views.lmsSignup,name="lmsSignup"),
    path('signup/IDSignup',views.idsignuppage,name="idsignuppage"),
    path('oauth/', views.oauth, name="oauth"),
    path('kakaologin/', views.kakoredirect, name="kakaologin"),
    path('calendar/', views.calendar, name = "calendar"),
    path('mypage/',views.mypage,name="mypage"),
    path('calendar/customize', views.customize, name = "customize"),
    path('home/', lms.views.home, name = "home"),
    path('mainLogin',views.mainLogin, name = "mainlogin"),
    path('',views.logout,name="logout"), # 초기화면 때문에 include 처리 안함
]