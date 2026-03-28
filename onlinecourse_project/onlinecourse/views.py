from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from .models import Course, Question, Choice, Submission

User = get_user_model()


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

    selected_choice_ids = [int(choice_id) for choice_id in request.POST.getlist('choice') if choice_id.isdigit()]
    selected_choices = Choice.objects.filter(pk__in=selected_choice_ids)
    questions = Question.objects.filter(lesson__course=course).prefetch_related('choice_set')

    submission_user = request.user if request.user.is_authenticated else None
    if submission_user is None:
        submission_user, created = User.objects.get_or_create(username='guest', defaults={'email': 'guest@example.com'})
        if created:
            submission_user.set_unusable_password()
            submission_user.save()

    submission = Submission.objects.create(user=submission_user)
    submission.choices.set(selected_choices)
    submission.save()

    return redirect('show_exam_result', course_id=course.id, submission_id=submission.id)


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    questions = Question.objects.filter(lesson__course=course).prefetch_related('choice_set')
    selected_choice_ids = submission.selected_choice_ids()
    question_results = submission.question_results(course)
    for question in questions:
        question.passed = question_results.get(question.id, False)

    score = submission.percentage(course)

    return render(request, 'onlinecourse/exam_result.html', {
        'course': course,
        'score': score,
        'correct': submission.correct_question_count(course),
        'total': submission.total_questions(course),
        'questions': questions,
        'selected_choice_ids': selected_choice_ids,
        'earned_grade': submission.earned_grade(course),
        'total_grade': submission.total_grade(course),
        'submission': submission,
    })
