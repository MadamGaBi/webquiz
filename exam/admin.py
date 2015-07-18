from django.contrib import admin
# Register your models here.
from .models import Tutor, Student, Topic, Question, Result, Answer
#_______________________________________________________________________________________________________________________

class QuestionInline(admin.TabularInline):
    model = Answer
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,             {'fields': ['tutor_id']}),
        (None,             {'fields': ['topic_id']}),
        ('Question',       {'fields': ['question_text']}),
    ]
    inlines = [QuestionInline]

    list_display = ('question_text', 'topic_id', 'tutor_id')
    list_filter = ['topic_id', 'tutor_id']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
#_______________________________________________________________________________________________________________________

class AnswerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,             {'fields': ['question_id']}),
        (None,             {'fields': ['is_correct']}),
        ('Answer',         {'fields': ['answer_text']}),
    ]

    list_display = ('answer_text','is_correct',  'question_id')
    list_filter = ['question_id']
    search_fields = ['answer_text']

admin.site.register(Answer, AnswerAdmin)
#_______________________________________________________________________________________________________________________

class ResultAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,             {'fields': ['student_id']}),
        (None,             {'fields': ['topic_id']}),
        ('Answer',         {'fields': ['mark']}),
    ]

    list_display = ('student_id','topic_id',  'mark')
    list_filter = ['student_id']
    search_fields = ['student_id']

admin.site.register(Result, ResultAdmin)
#_______________________________________________________________________________________________________________________

class StudentAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     (None,             {'fields': ['id']}),
    #     (None,             {'fields': ['username']}),
    #     (None,             {'fields': ['password']}),
    # ]
    pass
    # list_display = ('First name', 'Last name', 'id', 'username',  'password')
    # list_filter = ['id']
    # search_fields = ['student_id']

admin.site.register(Student, StudentAdmin)
#_______________________________________________________________________________________________________________________

admin.site.register(Topic)
admin.site.register(Tutor)



