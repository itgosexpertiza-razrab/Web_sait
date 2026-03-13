from django.db import models
from django.utils.html import mark_safe
from django.urls import reverse

class News(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=False)
    image = models.ImageField(upload_to="news/", blank=True, null=True)
    teaser = models.TextField()
    content = models.TextField()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"pk": self.pk})


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
    image = models.ImageField(upload_to="posts/", blank=True, null=True)

    def __str__(self):
        return self.title

    def content_safe(self):
        return mark_safe(self.content)

    def get_absolute_url(self):
        if self.category == "publication":
            return reverse("publication_detail", kwargs={"pk": self.pk})
        if self.category == "bim":
            return reverse("bim_detail", kwargs={"pk": self.pk})
        return reverse("home")


class Comment(models.Model):
    STATUS_CHOICES = [
        ("pending", "На модерации"),
        ("approved", "Одобрен"),
        ("rejected", "Отклонён"),
    ]

    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name="comments",
        blank=True,
        null=True,
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        blank=True,
        null=True,
    )

    author_name = models.CharField(max_length=120)
    author_email = models.EmailField(blank=True)
    text = models.TextField()

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    owner_reply = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    moderated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        target = self.news or self.post
        return f"Комментарий: {self.author_name} -> {target}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if not self.news and not self.post:
            raise ValidationError("Комментарий должен относиться либо к новости, либо к публикации.")
        if self.news and self.post:
            raise ValidationError("Комментарий не может одновременно относиться и к новости, и к публикации.")

