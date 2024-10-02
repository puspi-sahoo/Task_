from rest_framework import serializers
from .models import User, Exam, Question, Answer



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            role=validated_data['role'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class QuestionSerializerForStudent(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'options']

class QuestionSerializerForAdmin(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'options', 'correct_answer']

class ExamSerializerForStudent(serializers.ModelSerializer):
    questions = QuestionSerializerForStudent(many=True)

    class Meta:
        model = Exam
        fields = ['id', 'name', 'questions']

class ExamSerializerForAdmin(serializers.ModelSerializer):
    questions = QuestionSerializerForAdmin(many=True)

    class Meta:
        model = Exam
        fields = ['id', 'name', 'questions']

    def create(self, validated_data):
        questions_data = validated_data.pop('questions')
        exam = Exam.objects.create(**validated_data)
        for question_data in questions_data:
            Question.objects.create(exam=exam, **question_data)
        return exam

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
