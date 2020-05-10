from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    #Admin page remove after complition

    path('admin/', admin.site.urls),

    #User managment
    
    path('accounts/', include('allauth.urls')),

    #Local apps
    path('', include('main.urls')),
    path('profile/', include('users.urls'))
    
]
