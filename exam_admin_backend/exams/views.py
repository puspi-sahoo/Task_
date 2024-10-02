from rest_framework import generics, permissions
from .models import Exam, Question, Answer
from .serializers import ExamSerializerForStudent, ExamSerializerForAdmin, QuestionSerializerForStudent, QuestionSerializerForAdmin, AnswerSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist



class CreateUserView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExamListCreateView(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return ExamSerializerForAdmin
        return ExamSerializerForStudent

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only admins can create exams.")
        serializer.save(created_by=self.request.user)


class ExamDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, exam_id):
        exam = get_object_or_404(Exam, id=exam_id)
        if request.user.is_staff:
            serializer = ExamSerializerForAdmin(exam)
        else:
            serializer = ExamSerializerForStudent(exam)
        return Response(serializer.data)


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return QuestionSerializerForAdmin
        return QuestionSerializerForStudent

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only admins can create questions.")
        serializer.save()


class AnswerSubmitView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        answers_data = request.data.get('answers')
        exam_id = request.data.get('exam_id')

        if not answers_data or len(answers_data) == 0:
            return Response({
                'error': 'No answers submitted.'
            }, status=status.HTTP_400_BAD_REQUEST)

        total_questions = len(answers_data)
        correct_answers = 0

        for question_id, answer_text in answers_data.items():
            try:
                question = Question.objects.get(id=question_id)
            except ObjectDoesNotExist:
                return Response({
                    'error': f'Question with ID {question_id} does not exist.'
                }, status=status.HTTP_400_BAD_REQUEST)

            is_correct = question.correct_answer == answer_text
            if is_correct:
                correct_answers += 1

            Answer.objects.create(
                question=question,
                student=request.user,
                answer_text=answer_text,
                is_correct=is_correct
            )

        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        result = 'Pass' if score >= 50 else 'Fail'

        return Response({
            'score': score,
            'result': result,
        }, status=status.HTTP_201_CREATED)
