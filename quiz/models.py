from django.db import models

class Direction(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название направления")
    api_category_id = models.IntegerField(verbose_name="ID категории OpenTriviaDB", blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Направление"
        verbose_name_plural = "Направления"

class Question(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField(verbose_name="Текст вопроса")
    option1 = models.CharField(max_length=500, verbose_name="Вариант 1")
    option2 = models.CharField(max_length=500, verbose_name="Вариант 2")
    option3 = models.CharField(max_length=500, verbose_name="Вариант 3")
    option4 = models.CharField(max_length=500, verbose_name="Вариант 4")
    correct_option = models.IntegerField(verbose_name="Правильный вариант (1-4)")
    
    def __str__(self):
        return self.text[:50]
    
    def get_options(self):
        return [self.option1, self.option2, self.option3, self.option4]
    
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

class QuizResult(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=100)
    correct_answers = models.IntegerField()
    total_questions = models.IntegerField()
    time_spent_seconds = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def percentage(self):
        if self.total_questions > 0:
            return int((self.correct_answers / self.total_questions) * 100)
        return 0
    
    def status(self):
        percent = self.percentage()
        if percent >= 80:
            return "Отлично"
        elif percent >= 60:
            return "Хорошо"
        elif percent >= 40:
            return "Средне"
        else:
            return "Нужно подтянуть"