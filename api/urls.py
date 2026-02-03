from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# 1. Создаем роутер
router = DefaultRouter()

# 2. Регистрируем в нем все наши ViewSet'ы
# Первый параметр - это часть URL, второй - сам ViewSet
router.register(r'profiles', views.ProfileViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.PostCommentViewSet)

# Образование
router.register(r'education-themes', views.EducationThemeViewSet)
router.register(r'student-questions', views.StudentQuestionViewSet)
router.register(r'student-answers', views.StudentAnswerViewSet)

# Общение
router.register(r'chat-rooms', views.ChatRoomViewSet)
router.register(r'chat-messages', views.ChatMessageViewSet)

# События
router.register(r'events', views.EventViewSet)

# 3. Включаем сгенерированные ссылки в urlpatterns
urlpatterns = [
    path('register/', views.register_demo_user, name='register-demo'),
    path('', include(router.urls)),
]