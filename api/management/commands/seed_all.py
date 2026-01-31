from django.core.management.base import BaseCommand
from api.models import Post, EducationTheme, Event

class Command(BaseCommand):
    def handle(self, *args, **options):
        # 1. Образование (п. 3.4)
        EducationTheme.objects.get_or_create(
            title="Теорема Пифагора",
            theory="a² + b² = c². Квадрат гипотенузы равен сумме квадратов катетов.",
            video_url="https://youtu.be/dQw4w9WgXcQ"
        )
        # 2. Новости (п. 3.2)
        Post.objects.get_or_create(
            content_type='news', author_name="CrewUp",
            text="В Бишкеке открылась новая скейт-площадка! Ждем всех в Ататюрке."
        )
        self.stdout.write("Контент из ТЗ загружен!")