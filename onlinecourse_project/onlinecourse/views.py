from django.shortcuts import render, get_object_or_404
from .models import Course, Question, Choice


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'onlinecourse/course_list.html', {'courses': courses})


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    lessons = course.lesson_set.all()
    questions = Question.objects.filter(lesson__course=course).prefetch_related('choice_set')
    return render(request, 'onlinecourse/course_detail.html', {
        'course': course,
        'lessons': lessons,
        'questions': questions,
    })


def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method != 'POST':
        return course_detail(request, course_id)

    selected_choices = request.POST.getlist('choice')
    correct_answers = 0
    for choice_id in selected_choices:
        try:
            choice = Choice.objects.get(pk=choice_id)
        except Choice.DoesNotExist:
            continue
        if choice.is_correct:
            correct_answers += 1

    total_questions = Question.objects.filter(lesson__course=course).count()
    score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0

    return render(request, 'onlinecourse/exam_result.html', {
        'course': course,
        'score': score,
        'correct': correct_answers,
        'total': total_questions,
    })


def show_exam_result(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'onlinecourse/exam_result.html', {
        'course': course,
        'score': None,
        'correct': 0,
        'total': 0,
    })
