from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', help_text='Автор')
    title = models.CharField(max_length=200, help_text='Название')
    image = models.ImageField(upload_to='foodgram_images/', help_text='Изображение')