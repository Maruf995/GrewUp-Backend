from rest_framework import serializers
from .models import (
    Profile, Post, PostComment, 
    EducationTheme, EducationTestQuestion, 
    StudentQuestion, StudentAnswer, 
    ChatRoom, ChatMessage, 
    Event
)

# --- 1. ПРОФИЛЬ ---
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'id', 'nickname', 'region', 'avatar', 
            'interests', 'xp', 'level', 'is_founder'
        ]
        read_only_fields = ['xp', 'level', 'is_founder'] 
        # XP и уровень меняются только через специальные действия, а не прямым редактированием


# --- 2. ЛЕНТА И КОММЕНТАРИИ ---
class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ['id', 'author_name', 'text', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    # Вкладываем комментарии внутрь поста
    comments = PostCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'content_type', 'author_name', 'text', 
            'image', 'poll_data', 'likes', 'created_at', 
            'comments'
        ]


# --- 3. ОБРАЗОВАНИЕ ---
class EducationTestQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationTestQuestion
        fields = ['id', 'question_text', 'options', 'correct_option_index']

class EducationThemeSerializer(serializers.ModelSerializer):
    # Вкладываем вопросы теста внутрь темы
    questions = EducationTestQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = EducationTheme
        fields = [
            'id', 'title', 'theory', 'video_url', 
            'subject', 'grade', 'questions'
        ]


# --- 4. ВОПРОСЫ СТУДЕНТОВ (Q&A) ---
class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ['id', 'author_name', 'text', 'is_best', 'created_at']

class StudentQuestionSerializer(serializers.ModelSerializer):
    # Вкладываем ответы внутрь вопроса
    answers = StudentAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = StudentQuestion
        fields = [
            'id', 'author_name', 'subject', 'text', 
            'reward_xp', 'created_at', 'answers'
        ]


# --- 5. ЧАТЫ ---
class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'author_name', 'text', 'is_preloaded', 'created_at']

class ChatRoomSerializer(serializers.ModelSerializer):
    # Для списка комнат сообщения можно не грузить, но для демо удобно видеть сразу
    # Если сообщений будет 1000, это место нужно переделать. Для демо (5-10 сообщений) — ок.
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatRoom
        fields = ['id', 'title', 'room_type', 'tag', 'messages']


# --- 6. СОБЫТИЯ ---
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date_str', 'location', 'image']