from django.contrib import admin
from .models import User, Exam, Question, Answer


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')
    ordering = ('username',)

class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by')
    search_fields = ('name',)
    list_filter = ('created_by',)
    ordering = ('name',)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'exam', 'correct_answer')
    search_fields = ('question_text',)
    list_filter = ('exam',)
    ordering = ('exam',)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'answer_text', 'is_correct')
    search_fields = ('student__username', 'question__question_text', 'answer_text')
    list_filter = ('is_correct',)
    ordering = ('student',)

admin.site.register(User, UserAdmin)
admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
