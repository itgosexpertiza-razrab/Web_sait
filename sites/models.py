from django.db import models
from django.utils.html import mark_safe

class News(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=False)
    image = models.ImageField(upload_to='news/')
    teaser = models.TextField()
    content = models.TextField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title


class HelpItem(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return self.title


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('news', 'Новости'),
        ('publication', 'Публикации'),
        ('bim', 'BIM технологии'),
        ('map', 'Картограмма'),
    ]


    title = models.CharField(max_length=255)
    date = models.DateField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    intro = models.TextField(blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True)

    def __str__(self):
        return self.title

    def content_safe(self):
        return mark_safe(self.content)

    def get_absolute_url(self):
        return f"/{self.category}/{self.id}/"

