from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import (
    Profile, Post, PostComment,
    EducationTheme, StudentQuestion, StudentAnswer,
    ChatRoom, ChatMessage, Event
)
from .serializers import (
    ProfileSerializer, PostSerializer, PostCommentSerializer,
    EducationThemeSerializer, StudentQuestionSerializer, StudentAnswerSerializer,
    ChatRoomSerializer, ChatMessageSerializer, EventSerializer
)

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
    
    # Включаем возможность сортировки (для Топ-3: /api/profiles/?ordering=-xp)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['xp', 'level']

    @action(detail=True, methods=['post'])
    def add_xp(self, request, pk=None):
        """Начислить XP (симуляция активности)"""
        profile = self.get_object()
        try:
            amount = int(request.data.get('amount', 10))
        except ValueError:
            return Response({"error": "Amount must be a number"}, status=status.HTTP_400_BAD_REQUEST)
            
        profile.add_xp(amount)
        return Response({
            'status': 'XP added', 
            'new_xp': profile.xp, 
            'new_level': profile.level
        })

    @action(detail=True, methods=['post'])
    def reset_demo(self, request, pk=None):
        """Сброс прогресса пользователя (для повторной презентации)"""
        profile = self.get_object()
        # 1. Сбрасываем уровень и XP до дефолтных
        profile.xp = 50
        profile.level = 1
        profile.save()
        
        # 2. Здесь можно добавить очистку постов пользователя, если нужно
        
        return Response({
            'status': 'Demo Reset Successful', 
            'xp': profile.xp, 
            'level': profile.level
        })


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        content_type = self.request.query_params.get('type')
        if content_type:
            queryset = queryset.filter(content_type=content_type)
        return queryset


class PostCommentViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = [permissions.AllowAny]


class EducationThemeViewSet(viewsets.ModelViewSet):
    queryset = EducationTheme.objects.all()
    serializer_class = EducationThemeSerializer
    permission_classes = [permissions.AllowAny]


class StudentQuestionViewSet(viewsets.ModelViewSet):
    queryset = StudentQuestion.objects.all().order_by('-created_at')
    serializer_class = StudentQuestionSerializer
    permission_classes = [permissions.AllowAny]


class StudentAnswerViewSet(viewsets.ModelViewSet):
    queryset = StudentAnswer.objects.all()
    serializer_class = StudentAnswerSerializer
    permission_classes = [permissions.AllowAny]


class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        room_type = self.request.query_params.get('type')
        tag = self.request.query_params.get('tag')
        if room_type:
            queryset = queryset.filter(room_type=room_type)
        if tag:
            queryset = queryset.filter(tag=tag)
        return queryset

@api_view(['POST'])
@permission_classes([AllowAny])
def register_demo_user(request):
    """
    Быстрая регистрация для демо.
    Принимает JSON: {
        "nickname": "Syrgak",
        "region": "Bishkek",
        "avatar_id": "avatar_1.png",  # или индекс
        "interests": ["games", "sport"]
    }
    """
    data = request.data
    nickname = data.get('nickname')

    if not nickname:
        return Response({'error': 'Никнейм обязателен'}, status=400)

    # 1. Создаем пользователя (пароль ставим заглушку, он не нужен для демо)
    if User.objects.filter(username=nickname).exists():
        return Response({'error': 'Такой ник уже занят, выбери другой'}, status=400)
    
    user = User.objects.create_user(username=nickname, password='demo_password_123')

    # 2. Создаем профиль
    profile = Profile.objects.create(
        user=user,
        nickname=nickname,
        region=data.get('region', 'Bishkek'),
        # Фронт может присылать имя файла или ID, тут сохраняем как есть
        # Если фронт шлет файл, логика другая, но для демо проще слать строку-идентификатор
        interests=data.get('interests', [])
    )
    
    # Если фронт шлет реальный файл аватара через multipart/form-data, 
    # то profile.avatar = request.FILES['avatar']

    return Response({
        'status': 'created',
        'user_id': user.id,
        'profile_id': profile.id,
        'nickname': profile.nickname
    })

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all().order_by('created_at')
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.AllowAny]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

