from django.urls import path
from characters.views import character_page, character_creation_page, character_list

urlpatterns = [
    path('create/', character_creation_page, name='character_creation_page'),
    path('list/', character_list, name='character_list'),
    path('char-id-<int:character_id>/', character_page, name='character_page'),
    path('<str:character_name>/', character_page, name='character_page')
]
