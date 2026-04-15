from django.core.management.base import BaseCommand
from quiz.models import Direction, Question

class Command(BaseCommand):
    help = 'Загружает русские вопросы для тестирования'
    
    def handle(self, *args, **kwargs):
        directions = ["Python", "JavaScript", "Java"]
        
        for direction_name in directions:
            direction, created = Direction.objects.get_or_create(
                name=direction_name,
                defaults={"api_category_id": 0}
            )
            
            if Question.objects.filter(direction=direction).count() == 0:
                self.stdout.write(f"Создание вопросов для {direction_name}...")
                self.create_questions_for_direction(direction)
            else:
                self.stdout.write(f"Вопросы для {direction_name} уже есть ({Question.objects.filter(direction=direction).count()} шт.)")
    
    def create_questions_for_direction(self, direction):
        """Создает 10 вопросов для направления"""
        
        if direction.name == "Python":
            questions = [
                ("Что такое Python?", "Язык программирования", "База данных", "Операционная система", "Браузер", 1),
                ("Какой символ используется для комментариев в Python?", "#", "//", "/*", "--", 1),
                ("Какой метод используется для вывода в консоль в Python?", "print()", "console.log()", "echo()", "System.out.println()", 1),
                ("Что такое PEP 8?", "Стандарт оформления кода", "Библиотека", "Фреймворк", "База данных", 1),
                ("Какой тип данных используется для хранения целых чисел в Python?", "int", "str", "float", "bool", 1),
                ("Что делает функция len()?", "Возвращает длину объекта", "Выводит данные", "Создает список", "Удаляет элемент", 1),
                ("Какой фреймворк используется для веб-разработки на Python?", "Django", "React", "Angular", "Vue", 1),
                ("Что такое list comprehension?", "Генератор списков", "Функция", "Класс", "Модуль", 1),
                ("Какой оператор используется для создания цикла for?", "for", "while", "loop", "iterate", 1),
                ("Что такое pip?", "Менеджер пакетов Python", "Библиотека", "Фреймворк", "IDE", 1),
            ]
        elif direction.name == "JavaScript":
            questions = [
                ("Какой символ используется для комментариев в JavaScript?", "//", "#", "<!--", "'''", 1),
                ("Что такое DOM?", "Объектная модель документа", "База данных", "Операционная система", "Браузер", 1),
                ("Какой метод используется для вывода в консоль в JavaScript?", "console.log()", "print()", "echo()", "System.out.println()", 1),
                ("Что такое React?", "Библиотека для UI", "База данных", "Операционная система", "Язык программирования", 1),
                ("Какой оператор используется для строгого сравнения в JS?", "===", "==", "=", "!=", 1),
                ("Что такое Node.js?", "Среда выполнения JS", "Библиотека", "Фреймворк", "База данных", 1),
                ("Как объявить переменную в JS?", "let", "var", "const", "Все варианты", 4),
                ("Что такое JSON?", "Формат обмена данными", "Язык программирования", "База данных", "Браузер", 1),
                ("Что делает метод map()?", "Преобразует массив", "Фильтрует массив", "Сортирует массив", "Удаляет элементы", 1),
                ("Что такое Promise в JS?", "Объект для асинхронных операций", "Функция", "Класс", "Массив", 1),
            ]
        elif direction.name == "Java":
            questions = [
                ("Что такое Java?", "Язык программирования", "База данных", "Операционная система", "Браузер", 1),
                ("Что такое JVM?", "Виртуальная машина Java", "Фреймворк", "Библиотека", "IDE", 1),
                ("Какой метод является точкой входа в Java-программе?", "main()", "start()", "run()", "init()", 1),
                ("Что такое OOP?", "Объектно-ориентированное программирование", "База данных", "Операционная система", "Фреймворк", 1),
                ("Что такое Spring?", "Фреймворк для Java", "Библиотека", "База данных", "IDE", 1),
                ("Какой тип данных используется для целых чисел в Java?", "int", "Integer", "Оба варианта", "number", 3),
                ("Что такое Maven?", "Инструмент сборки", "База данных", "Фреймворк", "IDE", 1),
                ("Что означает 'public static void main'?", "Точка входа", "Переменная", "Класс", "Метод", 1),
                ("Что такое наследование в Java?", "Механизм ООП", "Функция", "Класс", "Интерфейс", 1),
                ("Что такое интерфейс в Java?", "Абстрактный тип", "Класс", "Метод", "Переменная", 1),
            ]
        else:
            return
        
        for text, opt1, opt2, opt3, opt4, correct in questions:
            Question.objects.create(
                direction=direction,
                text=text,
                option1=opt1,
                option2=opt2,
                option3=opt3,
                option4=opt4,
                correct_option=correct
            )
        
        self.stdout.write(self.style.SUCCESS(f"  ✓ Создано {len(questions)} вопросов для {direction.name}"))