from django.urls import path
from .views import (
    HomeView,
    NewsListView, NewsDetailView, NewsCreateView, NewsUpdateView, NewsDeleteView,
    PublicationListView, BIMListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView,
    CommentCreateForNewsView, CommentCreateForPostView,
    CommentModerationListView, CommentModerationUpdateView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    path("news/", NewsListView.as_view(), name="news"),
    path("news/add/", NewsCreateView.as_view(), name="news_add"),
    path("news/<int:pk>/", NewsDetailView.as_view(), name="news_detail"),
    path("news/<int:pk>/edit/", NewsUpdateView.as_view(), name="news_edit"),
    path("news/<int:pk>/delete/", NewsDeleteView.as_view(), name="news_delete"),
    path("news/<int:pk>/comment/", CommentCreateForNewsView.as_view(), name="news_comment_add"),

    path("publication/", PublicationListView.as_view(), name="publication"),
    path("publication/add/", PostCreateView.as_view(), name="post_add"),
    path("publication/<int:pk>/", PostDetailView.as_view(), name="publication_detail"),
    path("publication/<int:pk>/comment/", CommentCreateForPostView.as_view(), name="publication_comment_add"),

    path("bim/", BIMListView.as_view(), name="bim"),
    path("bim/<int:pk>/", PostDetailView.as_view(), name="bim_detail"),

    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="post_edit"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),

    path("moderation/comments/", CommentModerationListView.as_view(), name="comment_moderation"),
    path("moderation/comments/<int:pk>/", CommentModerationUpdateView.as_view(), name="comment_moderation_edit"),
]