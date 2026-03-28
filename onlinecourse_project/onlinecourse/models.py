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