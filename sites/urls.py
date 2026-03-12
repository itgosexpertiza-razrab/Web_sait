from django.urls import path
from .views import (
    HomeView,
    NewsListView, NewsDetailView,
    PublicationList, BIMList,
    PostDetailView,
    FAQView, ProcurementView, ContactsView,
    MapView, 
    NewsCreateView, NewsUpdateView, NewsDeleteView,
    PostImageUpdateView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="home"),

    # новости
    path("news/", NewsListView.as_view(), name="news_list"),
    path("news/<int:pk>/", NewsDetailView.as_view(), name="news_detail"),
    path("news/add/", NewsCreateView.as_view(), name="news_add"),
    path("news/<int:pk>/edit/", NewsUpdateView.as_view(), name="news_edit"),
    path("news/<int:pk>/delete/", NewsDeleteView.as_view(), name="news_delete"),

    path("publication/", PublicationList.as_view(), name="publication_list"),
    path("publication/<int:pk>/", PostDetailView.as_view(), name="publication_detail"),

    path("bim/", BIMList.as_view(), name="bim_list"),
    path("bim/<int:pk>/", PostDetailView.as_view(), name="bim_detail"),

    #path('map/', MapList.as_view(), name='map_list'),
    path('map/<int:pk>/', PostDetailView.as_view(), name='map_detail'),

    #path('node/<int:pk>/', NodeDetailView.as_view(), name='node_detail'),


    path("faq/", FAQView.as_view(), name="faq_list"),
    path("procurement/", ProcurementView.as_view(), name="procurement"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
] 
