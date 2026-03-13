from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import News, Post, HelpItem, Comment
from .forms import PostImageForm, NewsForm, PostForm, CommentForm, CommentModerationForm


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.filter(
            status="approved",
            parent__isnull=True
        ).order_by("-created_at")
        return context


class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = News
    form_class = NewsForm
    fields = ["title", "date", "teaser", "content", "image"]
    template_name = "sites/news_form.html"
    permission_required = "sites.add_news"
    success_url = reverse_lazy("news")


class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = News
    form_class = NewsForm
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

    # def get_queryset(self):
    #     queryset = Post.objects.all()

    #     if self.category:
    #         queryset = queryset.filter(category=self.category)

    #     return queryset.order_by("-date")

    def get_queryset(self):
        qs = Post.objects.all()
        if self.category:
            qs = qs.filter(category=self.category)
        return qs.order_by("-date")



class PostDetailView(DetailView):
    model = Post
    template_name = "sites/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["comments"] = self.object.comments.filter(
            status="approved",
            parent__isnull=True
        ).order_by("-created_at")
        return context


class PublicationListView(PostListView):
    template_name = "sites/publication.html"
    context_object_name = "posts"
    category = "publication"


class BIMListView(PostListView):
    template_name = "sites/bim.html"
    context_object_name = "posts"
    category = "bim"

class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "sites/post_form.html"
    permission_required = "sites.add_post"
    success_url = reverse_lazy("publication")


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "sites/post_form.html"
    permission_required = "sites.change_post"
    success_url = reverse_lazy("publication")


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = "sites/post_confirm_delete.html"
    permission_required = "sites.delete_post"
    success_url = reverse_lazy("publication")


class CommentCreateForNewsView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        news = get_object_or_404(News, pk=self.kwargs["pk"])
        form.instance.news = news
        form.instance.status = "pending"
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("news_detail", kwargs={"pk": self.kwargs["pk"]})


class CommentCreateForPostView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])
        form.instance.post = post
        form.instance.status = "pending"
        return super().form_valid(form)

    def get_success_url(self):
        category = self.object.post.category
        if category == "publication":
            return reverse_lazy("publication_detail", kwargs={"pk": self.kwargs["pk"]})
        return reverse_lazy("bim_detail", kwargs={"pk": self.kwargs["pk"]})


class CommentModerationListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Comment
    template_name = "sites/comment_moderation_list.html"
    context_object_name = "comments"
    permission_required = "sites.change_comment"

    def get_queryset(self):
        return Comment.objects.order_by("-created_at")


class CommentModerationUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentModerationForm
    template_name = "sites/comment_moderation_form.html"
    permission_required = "sites.change_comment"
    success_url = reverse_lazy("comment_moderation")

    def form_valid(self, form):
        form.instance.moderated_at = timezone.now()
        return super().form_valid(form)


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