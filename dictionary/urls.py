from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    #Admin page remove after complition

    path('admin/', admin.site.urls),

    #User managment
    
    path('accounts/', include('django.contrib.auth.urls')),

    #Local apps
    path('accounts/', include('users.urls')),
    path('', include('main.urls')),
    
]
