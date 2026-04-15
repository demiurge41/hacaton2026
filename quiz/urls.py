from django.urls import path
from . import views

app_name = 'quiz'

urlpatterns = [
    path('', views.index, name='index'),
    path('start/<int:direction_id>/', views.start_test, name='start_test'),
    path('question/<int:question_index>/', views.question_view, name='question'),  # <-- ЭТО ВАЖНО!
    path('submit-answer/', views.submit_answer, name='submit_answer'),
    path('finish/', views.finish_test, name='finish_test'),
    path('profile/', views.profile, name='profile'),
]