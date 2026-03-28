from django.shortcuts import render, get_object_or_404
from .models import Course, Submission, Choice

def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    selected_choices = request.POST.getlist('choice')
    correct_answers = 0

    for choice_id in selected_choices:
        choice = Choice.objects.get(id=choice_id)
        if choice.is_correct:
            correct_answers += 1

    total_questions = course.question_set.count()
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    context = {
        'course': course,
        'score': score,
    }
    return render(request, 'onlinecourse/exam_result.html', context)

def show_exam_result(request, submission_id):
    submission = get_object_or_404(Submission, id=submission_id)
    choices = submission.choices.all()

    total = len(choices)
    correct = sum([1 for c in choices if c.is_correct])

    score = (correct / total) * 100 if total > 0 else 0

    return render(request, 'onlinecourse/result.html', {
        'score': score,
        'correct': correct,
        'total': total
    })