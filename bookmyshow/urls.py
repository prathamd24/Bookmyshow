from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from movies import views as movie_views
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('movies/', include('movies.urls')),
    path('', user_views.home, name='home'),  # ✅ root goes to home
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
