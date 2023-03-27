from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('anime/top/', views.top, name='topanime'),
    path('anime/top/<int:page>/', views.top, name='top_page'),
    path('anime/<int:anime_id>/', views.detail, name='detail'),
    path('animelist/', views.animelist, name='animelist'),
    path('anime/<int:anime_id>/update_status/', views.update_anime_status, name='update_anime_status'),
    path('anime/<int:anime_id>/remove_from_list/', views.remove_anime_from_list, name='remove_anime_from_list'),
    path('submit_comment/<int:anime_id>/', views.submit_comment, name='submit_comment'),
    path('edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('search/', views.search, name='search'),
    path('search/<int:page>/', views.search, name='search_page'),
    path('anime/season/', views.seasonal, name='season'),
    path('anime/season/<int:page>/', views.seasonal, name='season_page'),
    path('search/anime', views.anime_search, name='anime_search'),
]