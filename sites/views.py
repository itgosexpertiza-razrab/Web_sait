from django.views.generic import TemplateView, ListView, DetailView
from .models import News, Post, HelpItem
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import PostImageForm

# =========================
# Главная
# =========================
class HomeView(TemplateView):
    template_name = 'sites/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['news'] = News.objects.all()[:10]
        ctx['help_items'] = HelpItem.objects.all()
        return ctx


# =========================
# Новости (отдельная модель)
# =========================
class NewsListView(ListView):
    model = News
    template_name = 'sites/news_list.html'
    context_object_name = 'news'
    paginate_by = 10

class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = News
    fields = ["title", "date", "content", "image"]
    template_name = "sites/news_form.html"
    permission_required = "sites.add_news"
    success_url = reverse_lazy("news_list")

class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = News
    fields = ["title", "date", "content", "image"]
    template_name = "sites/news_form.html"
    permission_required = "sites.change_news"
    success_url = reverse_lazy("news_list")

class PublicationView(ListView):
    model = Post
    template_name = 'sites/publication.html'
    context_object_name = 'publication'

    def get_queryset(self):
        return Post.objects.filter(category='publication')

class NewsView(ListView):
    model = News
    template_name = 'sites/news.html'
    context_object_name = 'news'

class NewsDetailView(DetailView):
    model = News
    template_name = 'sites/news_detail.html'
    context_object_name = 'news'

class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = News
    template_name = "sites/news_confirm_delete.html"
    permission_required = "sites.delete_news"
    success_url = reverse_lazy("news_list")

# =========================
# Универсальные Post
# =========================
class PostListView(ListView):
    model = Post
    template_name = "sites/post_list.html"
    context_object_name = "posts"
    category = None

    def get_queryset(self):
        return Post.objects.filter(category=self.category)


class PostDetailView(DetailView):
    model = Post
    template_name = "sites/post_detail.html"


class PublicationList(PostListView):
    category = "publication"


class BIMList(PostListView):
    category = "bim"


# =========================
# Статичные страницы
# =========================
class FAQView(TemplateView):
    template_name = "sites/faq.html"


class ProcurementView(TemplateView):
    template_name = "sites/procurement.html"


class ContactsView(TemplateView):
    template_name = "sites/contacts.html"


class MapView(TemplateView):
    template_name = "sites/map_placeholder.html"


class PostImageUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    model = Post
    form_class = PostImageForm
    template_name = "sites/post_image_edit.html"
    permission_required = "sites.change_post"

    def get_success_url(self):
        return self.object.get_absolute_url()