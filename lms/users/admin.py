from django.contrib import admin
from users.models import *
from contests.models import *

admin.site.register(Profile)
admin.site.register(Contest)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(AttendedQuestion)
admin.site.register(Section)
admin.site.register(TotalScore)
admin.site.register(Domain)
