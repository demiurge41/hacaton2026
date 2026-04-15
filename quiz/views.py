from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Direction, Question, QuizResult
import json
import time

def index(request):
    """Главная страница с выбором направления"""
    directions = Direction.objects.all()
    return render(request, 'quiz/index.html', {'directions': directions})

def start_test(request, direction_id):
    """Начать тест по выбранному направлению"""
    direction = get_object_or_404(Direction, id=direction_id)
    questions = list(direction.questions.all())
    
    if not questions:
        return redirect('quiz:index')
    
    # Сохраняем данные теста в сессии
    request.session['test_direction_id'] = direction_id
    request.session['test_questions'] = [q.id for q in questions]
    request.session['test_answers'] = {}
    request.session['test_start_time'] = time.time()
    request.session['current_question_index'] = 0
    
    return redirect('quiz:question', question_index=0)

def question_view(request, question_index):
    """Отображение вопроса"""
    if 'test_questions' not in request.session:
        return redirect('quiz:index')
    
    questions_ids = request.session['test_questions']
    
    if question_index >= len(questions_ids):
        return redirect('quiz:finish_test')
    
    question_id = questions_ids[question_index]
    question = get_object_or_404(Question, id=question_id)
    
    context = {
        'question': question,
        'question_number': question_index + 1,
        'total_questions': len(questions_ids),
        'progress': int((question_index / len(questions_ids)) * 100) if len(questions_ids) > 0 else 0
    }
    
    return render(request, 'quiz/test.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def submit_answer(request):
    """Сохраняет ответы пользователя"""
    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        selected_option = data.get('selected_option')
        
        if 'test_answers' not in request.session:
            request.session['test_answers'] = {}
        
        request.session['test_answers'][str(question_id)] = selected_option
        request.session.modified = True
        
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def finish_test(request):
    """Завершение теста и показ результатов"""
    if 'test_questions' not in request.session:
        return redirect('quiz:index')
    
    questions_ids = request.session['test_questions']
    answers = request.session.get('test_answers', {})
    start_time = request.session.get('test_start_time', time.time())
    
    # Подсчитывает правильные ответы
    correct_count = 0
    for q_id in questions_ids:
        try:
            question = Question.objects.get(id=q_id)
            user_answer = answers.get(str(q_id))
            
            if user_answer and int(user_answer) == question.correct_option:
                correct_count += 1
        except Question.DoesNotExist:
            pass
    
    time_spent = int(time.time() - start_time)
    
    # Сохраняет результат
    direction_id = request.session.get('test_direction_id')
    if direction_id:
        direction = get_object_or_404(Direction, id=direction_id)
        
        # Получаем или создаем session_key
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        result = QuizResult.objects.create(
            direction=direction,
            session_key=session_key,
            correct_answers=correct_count,
            total_questions=len(questions_ids),
            time_spent_seconds=time_spent
        )
    else:
        result = None
    
    # Очищает сессию теста
    for key in ['test_direction_id', 'test_questions', 'test_answers', 'test_start_time', 'current_question_index']:
        if key in request.session:
            del request.session[key]
    
    context = {
        'result': result,
        'percentage': result.percentage() if result else 0,
        'status': result.status() if result else "Ошибка",
        'minutes': time_spent // 60,
        'seconds': time_spent % 60,
        'correct_count': correct_count,
        'total_questions': len(questions_ids)
    }
    
    return render(request, 'quiz/result.html', context)

def profile(request):
    """Личный кабинет с историей результатов"""
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    
    results = QuizResult.objects.filter(session_key=session_key).order_by('-created_at')
    
    return render(request, 'quiz/profile.html', {'results': results})

def share_result(request, result_id):
    """Публичная страница результата для HR"""
    result = get_object_or_404(QuizResult, id=result_id)
    return render(request, 'quiz/share.html', {'result': result})