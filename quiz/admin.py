from django.contrib import admin
from .models import Direction, Question, QuizResult

@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'api_category_id')
    search_fields = ('name',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'direction', 'text', 'correct_option')
    list_filter = ('direction',)
    search_fields = ('text',)

@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'direction', 'session_key', 'correct_answers', 'total_questions', 'created_at')
    list_filter = ('direction', 'created_at')
    readonly_fields = ('created_at',)