from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),  
    path('user/', include('shop.user_urls')),
    path('admin-dashboard/', include('shop.admin_urls')),  # <-- ADD THIS



]
