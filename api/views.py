from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *

class CrewUpViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def register(self, request):
        data = request.data
        # Создаем пользователя или берем существующего для демо
        user, _ = User.objects.get_or_create(username=data['nickname'])
        profile, created = Profile.objects.get_or_create(
            user=user,
            nickname=data['nickname'],
            region=data['region'],
            avatar_url=data['avatar_url'],
            interests=data.get('interests', []),
            xp=50
        )
        return Response(ProfileSerializer(profile).data)

    @action(detail=False, methods=['post'])
    def do_action(self, request):
        # Начисление XP согласно ТЗ (п. 3.2 и 3.6)
        nickname = request.data.get('nickname')
        act = request.data.get('action') # 'post', 'poll', 'chat', 'quiz'
        profile = Profile.objects.get(nickname=nickname)

        rewards = {'post': 30, 'poll': 5, 'quiz': 10, 'chat': 10}
        xp_gain = rewards.get(act, 0)
        
        old_level = profile.level
        profile.add_xp(xp_gain)
        
        return Response({
            "xp_added": xp_gain,
            "current_xp": profile.xp,
            "level": profile.level,
            "level_up": profile.level > old_level
        })

    @action(detail=False, methods=['get'])
    def get_chats(self, request):
        nickname = request.query_params.get('nickname')
        profile = Profile.objects.get(nickname=nickname)
        
        chats = [{"name": "Анонимный чат", "type": "anon"}]
        # Логика землячеств по ТЗ (п. 3.5.3)
        if profile.region != "Бишкек":
            chats.append({"name": f"Земляки ({profile.region})", "type": "regional"})
        
        return Response(chats)

    @action(detail=False, methods=['post'])
    def reset_demo(self, request):
        # Кнопка сброса для админки (п. 3.8)
        nickname = request.data.get('nickname')
        Profile.objects.filter(nickname=nickname).update(xp=50, level=1)
        Post.objects.filter(author_name=nickname, content_type='feed').delete()
        return Response({"status": "Сброшено"})