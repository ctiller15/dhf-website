from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
    url(r"^", include("users.urls")),
    path('admin/', admin.site.urls),
    path('', include("search.urls")),
    path('characters/', include("characters.urls")),
    path('series/', include("series.urls"))
]
