from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static

urlpatterns = [
    url(r"^", include("users.urls")),
    path('admin/', admin.site.urls),
    path('', include("search.urls")),
    path('characters/', include("characters.urls")),
    path('series/', include("series.urls"))
]

if settings.DEBUG:
    print('debug!')
    print(settings.MEDIA_URL)
    print(settings.MEDIA_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
