from django.contrib import admin
from .models import Course, Lesson, Question, Choice, Submission, Instructor
from django.contrib.auth.models import User, Group

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]

class LessonAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ('name',)
    list_filter = ('lesson__title',)
    search_fields = ('name',)

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Submission)
admin.site.register(Instructor)