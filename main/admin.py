from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.QuizCategory)

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['question','que_level']

admin.site.register(models.QuizQuestion,QuizQuestionAdmin)

class UserSubmittedAnswerAdmin(admin.ModelAdmin):
    list_display = ['id','question','user','right_answer', 'usid']

admin.site.register(models.UserSubmittedAnswer,UserSubmittedAnswerAdmin)