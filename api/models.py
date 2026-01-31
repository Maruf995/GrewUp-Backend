from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField("Никнейм", max_length=50, unique=True)
    region = models.CharField("Регион", max_length=100)
    avatar_url = models.CharField("URL Аватара", max_length=255)
    interests = models.JSONField("Интересы", default=list)
    xp = models.IntegerField("Очки опыта", default=50) # Старт с 50 по ТЗ
    level = models.IntegerField("Уровень", default=1)
    is_founder = models.BooleanField("Статус Основателя", default=True)

    def add_xp(self, amount):
        self.xp += amount
        # Логика уровня по ТЗ: Уровень 2 при 100 XP
        if self.xp >= 100 and self.level < 2:
            self.level = 2
        self.save()

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

class Post(models.Model):
    TYPES = (('feed', 'Лента'), ('news', 'Новости'), ('poll', 'Опрос'))
    content_type = models.CharField("Тип", choices=TYPES, max_length=10)
    author_name = models.CharField("Автор", max_length=50)
    text = models.TextField("Текст", max_length=280)
    image_url = models.URLField("Картинка", blank=True, null=True)
    poll_results = models.JSONField("Результаты опроса", blank=True, null=True)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

class EducationTheme(models.Model):
    title = models.CharField("Тема", max_length=255)
    theory = models.TextField("Теория")
    video_url = models.URLField("Видео (YouTube)")
    subject = models.CharField("Предмет", max_length=50, default='Математика')
    grade = models.IntegerField("Класс", default=9)

class Event(models.Model):
    title = models.CharField("Заголовок", max_length=255)
    date = models.CharField("Дата", max_length=100)
    location = models.CharField("Место", max_length=255)