from django.db import models
from django.contrib.auth.models import User

# --- СПИСКИ ВЫБОРА (CHOICES) ---
REGION_CHOICES = (
    ('Bishkek', 'Бишкек'),
    ('Chuy', 'Чуйская обл.'),
    ('Osh', 'Ош'),
    ('Issyk-Kul', 'Иссык-Куль'),
    ('Naryn', 'Нарын'),
    ('Talas', 'Талас'),
    ('Jalal-Abad', 'Джалал-Абад'),
    ('Batken', 'Баткен'),
)

POST_TYPES = (
    ('feed', 'Лента'),
    ('news', 'Новости'),
    ('poll', 'Опрос'),
)

CHAT_TYPES = (
    ('anon', 'Анонимный'),
    ('interest', 'По интересам'),
    ('region', 'Землячество'),
)

# --- 1. ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField("Никнейм", max_length=50, unique=True)
    region = models.CharField("Регион", max_length=50, choices=REGION_CHOICES)
    avatar = models.ImageField("Аватар", upload_to='avatars/', blank=True, null=True)
    interests = models.JSONField("Интересы", default=list)
    
    # Геймификация
    xp = models.IntegerField("Очки опыта (XP)", default=50)
    level = models.IntegerField("Уровень", default=1)
    is_founder = models.BooleanField("Статус Основателя", default=True)

    def add_xp(self, amount):
        """Начисляет опыт и повышает уровень (Logic updated for Demo)"""
        self.xp += amount
        
        # Логика уровней по ТЗ:
        # Уровень 1: 0-99 XP
        # Уровень 2: 100-249 XP
        # Уровень 3: 250+ XP
        if self.xp >= 250:
            self.level = 3
        elif self.xp >= 100:
            self.level = 2
        
        self.save()

    def __str__(self):
        return f"{self.nickname} (Lvl {self.level})"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


# --- 2. ЛЕНТА, НОВОСТИ И ОПРОСЫ ---
class Post(models.Model):
    content_type = models.CharField("Тип контента", choices=POST_TYPES, max_length=10)
    author_name = models.CharField("Автор", max_length=50)
    text = models.TextField("Текст поста", max_length=500)
    image = models.ImageField("Картинка", upload_to='posts/', blank=True, null=True)
    poll_data = models.JSONField("Данные опроса", blank=True, null=True)
    likes = models.IntegerField("Лайки", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.get_content_type_display()}] {self.text[:30]}..."

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"


class PostComment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author_name = models.CharField("Автор", max_length=50)
    text = models.CharField("Комментарий", max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author_name}: {self.text[:20]}"


# --- 3. ОБРАЗОВАНИЕ ---
class EducationTheme(models.Model):
    title = models.CharField("Тема урока", max_length=255)
    theory = models.TextField("Теория")
    video_url = models.URLField("Видео (YouTube)", blank=True, null=True)
    subject = models.CharField("Предмет", max_length=50, default='Математика')
    grade = models.IntegerField("Класс", default=9)

    def __str__(self):
        return f"{self.subject} - {self.title}"

    class Meta:
        verbose_name = "Учебная тема"
        verbose_name_plural = "Учебные темы"


class EducationTestQuestion(models.Model):
    theme = models.ForeignKey(EducationTheme, related_name='questions', on_delete=models.CASCADE)
    question_text = models.CharField("Текст вопроса", max_length=500)
    options = models.JSONField("Варианты ответов") # ["A", "B", "C"]
    correct_option_index = models.IntegerField("Индекс правильного ответа")

    def __str__(self):
        return self.question_text[:50]


# --- 4. Q&A (ВОПРОСЫ СТУДЕНТОВ) ---
class StudentQuestion(models.Model):
    author_name = models.CharField("Автор", max_length=50)
    subject = models.CharField("Предмет", max_length=50)
    text = models.TextField("Текст вопроса")
    reward_xp = models.IntegerField("Награда (XP)", default=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = "Вопрос студента"
        verbose_name_plural = "Вопросы студентов"


class StudentAnswer(models.Model):
    question = models.ForeignKey(StudentQuestion, related_name='answers', on_delete=models.CASCADE)
    author_name = models.CharField("Автор", max_length=50)
    text = models.TextField("Текст ответа")
    is_best = models.BooleanField("Лучший ответ", default=False)
    # UPD: Добавлено поле рейтинга по ТЗ (напр. 4.8)
    rating = models.FloatField("Рейтинг", default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ответ от {self.author_name}"


# --- 5. ЧАТЫ ---
class ChatRoom(models.Model):
    title = models.CharField("Название комнаты", max_length=100)
    room_type = models.CharField("Тип", choices=CHAT_TYPES, max_length=20)
    tag = models.CharField("Тег", max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.get_room_type_display()})"

    class Meta:
        verbose_name = "Чат-комната"
        verbose_name_plural = "Чат-комнаты"


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, related_name='messages', on_delete=models.CASCADE)
    author_name = models.CharField("Автор", max_length=50)
    text = models.CharField("Сообщение", max_length=500)
    is_preloaded = models.BooleanField("Предзагружено", default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author_name}: {self.text[:20]}"


# --- 6. СОБЫТИЯ ---
class Event(models.Model):
    title = models.CharField("Название", max_length=255)
    description = models.TextField("Описание", blank=True)
    date_str = models.CharField("Дата (строка)", max_length=100)
    location = models.CharField("Место", max_length=255)
    image = models.ImageField("Картинка", upload_to='events/', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"