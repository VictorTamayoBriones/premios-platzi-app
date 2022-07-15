from django.contrib import admin

from polls.models import Choice, Question

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
    inlines = [ChoiceInline]
    list_display = ("question_text", "pub_date")
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    

admin.site.register(Question, QuestionAdmin)