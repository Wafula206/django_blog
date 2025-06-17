from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Your blog app routes
    path('', include('blogapp.urls')),

    # Built-in auth: login, password reset, etc.
    path('accounts/', include('django.contrib.auth.urls')),

    # Optional: custom logout with explicit next_page
    path('accounts/logout/', LogoutView.as_view(next_page='/accounts/login/'), name='logout'),
]

# Serve user-uploaded media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
