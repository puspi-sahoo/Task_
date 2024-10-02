from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='create-user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create_exam/', views.ExamListCreateView.as_view(), name='exam-list'),
    path('questions/', views.QuestionListCreateView.as_view(), name='question-list'),
    path('exam/<int:exam_id>/', views.ExamDetailView.as_view(), name='exam-detail'),
    path('submit_exam/', views.AnswerSubmitView.as_view(), name='submit-answer'),
]
