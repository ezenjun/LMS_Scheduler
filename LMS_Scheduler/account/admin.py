from django.contrib import admin
from .models import Account
from .models import *
# Register your models here.
admin.site.register(Account)
admin.site.register(Customer)
admin.site.register(Attendance)
admin.site.register(Class)
admin.site.register(Statistics)
admin.site.register(Priority)
admin.site.register(Calendercolor)
admin.site.register(Qna)
admin.site.register(Notices)