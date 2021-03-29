from django.contrib.auth.decorators import login_required
from characters.handlers.character_creation_page_handler import handle_character_creation
from characters.handlers.character_page_handler import handle_character_page
from characters.handlers.character_list_handler import handle_character_list
from characters.handlers.character_update_handler import handle_character_update

@login_required
def character_creation_page(request):
    response = handle_character_creation(request)
    return response

def character_page(request, character_name=None, character_id=None):
    response = handle_character_page(request, character_name, character_id)
    return response

def character_list(request):
    response = handle_character_list(request)
    return response

@login_required
def character_update(request):
    response = handle_character_update(request)
    return response
