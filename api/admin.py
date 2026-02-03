from django.contrib import admin
from .models import (
    Profile, Post, PostComment, 
    EducationTheme, EducationTestQuestion, 
    StudentQuestion, StudentAnswer, 
    ChatRoom, ChatMessage, Event
)

# 1. ПРОФИЛИ
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'user', 'region', 'level', 'xp', 'is_founder')
    list_filter = ('region', 'level', 'is_founder')
    search_fields = ('nickname', 'user__username')

# 2. ПОСТЫ + Комментарии внутри
class PostCommentInline(admin.TabularInline):
    model = PostComment
    extra = 1 # Сколько пустых строк показывать для добавления

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'content_type', 'author_name', 'likes', 'created_at')
    list_filter = ('content_type',)
    inlines = [PostCommentInline] # Комменты можно править прямо в Посте

@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'post', 'text', 'created_at')

# 3. ОБРАЗОВАНИЕ + Тесты внутри
class EducationTestQuestionInline(admin.StackedInline):
    model = EducationTestQuestion
    extra = 1

@admin.register(EducationTheme)
class EducationThemeAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'grade')
    list_filter = ('subject', 'grade')
    inlines = [EducationTestQuestionInline] # Вопросы теста добавляем здесь

@admin.register(EducationTestQuestion)
class EducationTestQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'theme')

# 4. ВОПРОСЫ Q&A + Ответы внутри
class StudentAnswerInline(admin.StackedInline):
    model = StudentAnswer
    extra = 1

@admin.register(StudentQuestion)
class StudentQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'author_name', 'subject', 'reward_xp')
    list_filter = ('subject',)
    inlines = [StudentAnswerInline]

# 5. ЧАТЫ + Сообщения внутри
class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 1

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'room_type', 'tag')
    list_filter = ('room_type',)
    inlines = [ChatMessageInline] # Предзагружать сообщения удобно тут

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'room', 'text', 'is_preloaded')
    list_filter = ('room', 'is_preloaded')

# 6. СОБЫТИЯ
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_str', 'location')