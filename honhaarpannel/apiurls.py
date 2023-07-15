from django.urls import path
from honhaarpannel import apiviews

urlpatterns = [
    path('schools/', apiviews.SchoolApi.as_view()),
    path('schools/<int:school_id>/', apiviews.SchoolApi.as_view()),
    path('batches/', apiviews.SchoolBatchApi.as_view()),
    path('batches/<int:batch_id>/', apiviews.BatchApi.as_view()),
    # path('schools/<int:school_id>/batches/', apiviews.SchoolBatchApi.as_view()),
    path('students/', apiviews.StudentBatchApi.as_view()),
    path('students/<int:student_id>/', apiviews.StudentApi.as_view()),
    path('settings/', apiviews.SettingApi.as_view()),
    path('matches/', apiviews.MatchApi.as_view()),
    path('schools/<int:school_id>/matches/', apiviews.SchoolMatchApi.as_view()),
    path('rounds/',apiviews.RoundApi.as_view()),
    path('rounds/<int:round_id>/',apiviews.RoundApi.as_view()),
    path('questions/',apiviews.QuestionApi.as_view()),
    path('questions/<int:question_id>/', apiviews.QuestionApi.as_view()),
    path('matchdetails/', apiviews.MatchesDetailsApi.as_view()),
    path('matches/<int:match_id>/', apiviews.MatchesDetailsApi.as_view()),

]
