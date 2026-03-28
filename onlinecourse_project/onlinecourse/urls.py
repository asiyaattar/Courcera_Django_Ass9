from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('submit/<int:course_id>/', views.submit, name='submit'),
    path('result/<int:course_id>/', views.show_exam_result, name='show_exam_result'),
]