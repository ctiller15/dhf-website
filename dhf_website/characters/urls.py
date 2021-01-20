from django.urls import path
from characters.views import character_page

urlpatterns = [
    path('<str:character_name>/', character_page, name='character_page')
]
