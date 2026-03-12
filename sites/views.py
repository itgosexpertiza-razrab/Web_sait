from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from .models import News, Post, HelpItem
from .forms import PostImageForm


# =========================
# Главная
# =========================
class HomeView(TemplateView):
    template_name = "sites/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["news"] = News.objects.order_by("-date")[:10]
        context["help_items"] = HelpItem.objects.all()
        return context


# =========================
# Новости
# =========================
class NewsListView(ListView):
    model = News
    template_name = "sites/news.html"
    context_object_name = "news"
    paginate_by = 10
    ordering = ["-date"]


class NewsDetailView(DetailView):
    model = News
    template_name = "sites/news_detail.html"
    context_object_name = "news"


class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = News
    fields = ["title", "date", "teaser", "content", "image"]
    template_name = "sites/news_form.html"
    permission_required = "sites.add_news"
    success_url = reverse_lazy("news")


class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = News
    fields = ["title", "date", "teaser", "content", "image"]
    template_name = "sites/news_form.html"
    permission_required = "sites.change_news"
    success_url = reverse_lazy("news")


class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = News
    template_name = "sites/news_confirm_delete.html"
    permission_required = "sites.delete_news"
    success_url = reverse_lazy("news")


# =========================
# Универсальные Post
# =========================
class PostListView(ListView):
    model = Post
    template_name = "sites/post_list.html"
    context_object_name = "posts"
    paginate_by = 10
    category = None

    def get_queryset(self):
        queryset = Post.objects.all()

        if self.category:
            queryset = queryset.filter(category=self.category)

        return queryset.order_by("-date")


class PostDetailView(DetailView):
    model = Post
    template_name = "sites/post_detail.html"
    context_object_name = "post"


class PublicationListView(PostListView):
    template_name = "sites/publication.html"
    context_object_name = "posts"
    category = "publication"


class BIMListView(PostListView):
    template_name = "sites/bim.html"
    context_object_name = "posts"
    category = "bim"


# =========================
# Статичные страницы
# =========================
class FAQView(TemplateView):
    template_name = "sites/faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["help_items"] = HelpItem.objects.all()
        return context


class ProcurementView(TemplateView):
    template_name = "sites/procurement.html"


class ContactsView(TemplateView):
    template_name = "sites/contacts.html"


class MapView(TemplateView):
    template_name = "sites/map_placeholder.html"


class AntiCorruptionView(TemplateView):
    template_name = "sites/anti_corruption.html"


class AboutView(TemplateView):
    template_name = "sites/about.html"


# =========================
# Редактирование изображения Post
# =========================
class PostImageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostImageForm
    template_name = "sites/post_image_edit.html"
    permission_required = "sites.change_post"

    def get_success_url(self):
        return self.object.get_absolute_url()