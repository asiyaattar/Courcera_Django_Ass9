from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.CharField(max_length=200)

class Instructor(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=500)
    grade = models.IntegerField(default=1)

    def is_get_score(self, selected_choice_ids):
        correct_choice_ids = set(self.choice_set.filter(is_correct=True).values_list('id', flat=True))
        selected_ids = set(selected_choice_ids) & set(self.choice_set.values_list('id', flat=True))
        return selected_ids == correct_choice_ids

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choices = models.ManyToManyField(Choice)

    def __str__(self):
        return f"Submission {self.id} by {self.user}"

    def selected_choice_ids(self):
        return list(self.choices.values_list('id', flat=True))

    def question_results(self, course):
        questions = Question.objects.filter(lesson__course=course).prefetch_related('choice_set')
        selected_ids = self.selected_choice_ids()
        return {question.id: question.is_get_score(selected_ids) for question in questions}

    def total_questions(self, course):
        return Question.objects.filter(lesson__course=course).count()

    def correct_question_count(self, course):
        return sum(1 for passed in self.question_results(course).values() if passed)

    def total_grade(self, course):
        return sum(question.grade for question in Question.objects.filter(lesson__course=course))

    def earned_grade(self, course):
        return sum(question.grade for question, passed in self.question_results(course).items() if passed)

    def percentage(self, course):
        total_grade = self.total_grade(course)
        if total_grade == 0:
            return 0
        return (self.earned_grade(course) / total_grade) * 100
