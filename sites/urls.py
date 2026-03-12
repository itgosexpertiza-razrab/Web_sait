from django.urls import path
from .views import (
    HomeView,
    NewsListView,
    NewsDetailView,
    NewsCreateView,
    NewsUpdateView,
    NewsDeleteView,
    PublicationListView,
    BIMListView,
    PostDetailView,
    FAQView,
    ProcurementView,
    ContactsView,
    MapView,
    AntiCorruptionView,
    AboutView,
    PostImageUpdateView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    path("news/", NewsListView.as_view(), name="news"),
    path("news/<int:pk>/", NewsDetailView.as_view(), name="news_detail"),
    path("news/add/", NewsCreateView.as_view(), name="news_add"),
    path("news/<int:pk>/edit/", NewsUpdateView.as_view(), name="news_edit"),
    path("news/<int:pk>/delete/", NewsDeleteView.as_view(), name="news_delete"),

    path("publication/", PublicationListView.as_view(), name="publication"),
    path("publication/<int:pk>/", PostDetailView.as_view(), name="publication_detail"),

    path("bim/", BIMListView.as_view(), name="bim"),
    path("bim/<int:pk>/", PostDetailView.as_view(), name="bim_detail"),

    path("faq/", FAQView.as_view(), name="faq"),
    path("procurement/", ProcurementView.as_view(), name="procurement"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("map/", MapView.as_view(), name="map"),
    path("about/", AboutView.as_view(), name="about"),
    path("anti-corruption/", AntiCorruptionView.as_view(), name="anti_corruption"),

    path("post/<int:pk>/image-edit/", PostImageUpdateView.as_view(), name="post_image_edit"),
]